"""
SC Audit command line interface.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt
from pathlib import Path
import shutil

import click

from sc_audit import migrations
from sc_audit.backup.download import download_compatible_dumps
from sc_audit.backup.dump import dump_table, get_table_names
from sc_audit.backup.restore import TABLE_LOADING_ORDER, get_table_row_counts, restore_all_tables, restore_table
from sc_audit.loader.__main__ import catch_up_from_sources
from sc_audit.loader.distribution_outflows import load_distribution_txs
from sc_audit.loader.get_latest import get_latest_attr
from sc_audit.loader.impact_projects import load_impact_projects
from sc_audit.loader.minted_blocks import load_minted_blocks
from sc_audit.loader.retirement_from_block import load_retirement_from_block
from sc_audit.loader.retirements import load_retirements
from sc_audit.loader.sink_events import load_sink_events
from sc_audit.loader.sink_status import load_sink_statuses
from sc_audit.loader.sinking_txs import load_sinking_txs
from sc_audit.sources.sink_events import MercuryError
from sc_audit.views.inventory import view_inventory
from sc_audit.views.retirement import view_retirements
from sc_audit.views.sink_status import view_sinking_txs
from sc_audit.views.utils import format_df


@click.group()
@click.version_option(package_name="sc_audit")
def cli():
    """CLI for Stellarcarbon Audit tool"""
    pass


@cli.command(name="catch-up")
@click.option("--fresh", is_flag=True, help="Don't bootstrap loading from a backup")
def db_catch_up(fresh: bool):
    """Let the DB catch up with the data sources"""
    if not fresh and not all(get_table_row_counts().values()):
        click.echo("Downloading database dumps...")
        download_dir = download_compatible_dumps()
        restore_all_tables(download_dir)
        shutil.rmtree(download_dir)
    
    catch_up_from_sources()

# VIEWS

@cli.group()
def view():
    """View the state of Stellarcarbon assets and transactions"""
    pass

view_format = click.Option(
    ["-f", "--format"],
    default="df",
    type=click.Choice(['df', 'csv', 'json'], case_sensitive=False),
    help="The output format for this view",
    show_default=True,
)

@view.command(name="inventory", params=[view_format])
@click.option("--omit-empty", is_flag=True, help="Don't show empty minted blocks")
@click.option(
    "--until-date", 
    type=click.DateTime(formats=["%Y-%m-%d"]), 
    help="Reconstruct the inventory on the given date"
)
def cli_view_inventory(omit_empty: bool, until_date: dt.datetime | None, format: str):
    """View Stellarcarbon's current or historical inventory of eco-credits"""
    until_dt_date = until_date.date() if until_date else None
    mbdf = view_inventory(omit_empty=omit_empty, until_date=until_dt_date)
    click.echo(format_df(mbdf, format=format))


@view.command(name="retirements", params=[view_format])
@click.option("--beneficiary", help="Only show retirements for the given beneficiary address")
@click.option(
    "--from-date", 
    type=click.DateTime(formats=["%Y-%m-%d"]), 
    help="Filter retirements that happened on or after the given date"
)
@click.option(
    "--before-date", 
    type=click.DateTime(formats=["%Y-%m-%d"]), 
    help="Filter retirements that happened before the given date"
)
@click.option("--project", type=int, help="Filter by impact project")
def cli_view_retirements(
        beneficiary: str | None, 
        from_date: dt.datetime | None,
        before_date: dt.datetime | None,
        project: int | None,
        format: str,
    ):
    """View finalized retirements and the attributes of the retired credits"""
    from_dt_date = from_date.date() if from_date else None
    before_dt_date = before_date.date() if before_date else None
    rtdf = view_retirements(
        for_beneficiary=beneficiary,
        from_date=from_dt_date,
        before_date=before_dt_date,
        project=project,
    )
    click.echo(format_df(rtdf, format=format))


@view.command(name="sink", params=[view_format])
@click.option("--funder", help="Only show transactions for the given funder address")
@click.option("--recipient", help="Only show transactions for the given recipient address")
@click.option(
    "--from-date", 
    type=click.DateTime(formats=["%Y-%m-%d"]), 
    help="Filter transactions that happened on or after the given date"
)
@click.option(
    "--before-date", 
    type=click.DateTime(formats=["%Y-%m-%d"]), 
    help="Filter transactions that happened before the given date"
)
@click.option("--finalized", type=bool, help="Filter by retirement status")
def cli_view_sink_status(
        funder: str | None,
        recipient: str | None, 
        from_date: dt.datetime | None,
        before_date: dt.datetime | None,
        finalized: bool | None,
        format: str,
    ):
    """View sinking transactions and their retirement status"""
    from_dt_date = from_date.date() if from_date else None
    before_dt_date = before_date.date() if before_date else None
    txdf = view_sinking_txs(
        for_funder=funder,
        for_recipient=recipient,
        from_date=from_dt_date,
        before_date=before_dt_date,
        finalized=finalized,
    )
    click.echo(format_df(txdf, format=format))

# LOADING

@cli.group()
def load():
    """Load data from their original sources"""
    pass


@load.command(name="impact-projects")
def db_load_impact_projects():
    """Load impact projects into the DB"""
    num_impact_projects = load_impact_projects()
    click.echo(f"Loaded {num_impact_projects} impact projects")


@load.command(name="minted-blocks")
def db_load_minted_blocks():
    """Load minted blocks into the DB"""
    mint_cursor = get_latest_attr('mint_tx')
    num_minting_txs = load_minted_blocks(cursor=mint_cursor) # type: ignore[arg-type]
    click.echo(f"Loaded {num_minting_txs} minted blocks")


@load.command(name="distribution-txs")
def db_load_distribution_outflows():
    """Load distribution outflows into the DB"""
    dist_cursor = get_latest_attr('dist_tx')
    num_distribution_txs = load_distribution_txs(cursor=dist_cursor) # type: ignore[arg-type]
    click.echo(f"Loaded {num_distribution_txs} distribution outflows")


@load.command(name="sinking-txs")
def db_load_sinking_txs():
    """Load sinking transactions into the DB"""
    sink_cursor: int = get_latest_attr('sink_tx') # type: ignore[return-value]
    num_sinking_txs = load_sinking_txs(cursor=sink_cursor)
    click.echo(f"Loaded {num_sinking_txs} sinking transactions")
    try:
        num_sink_events, _ = load_sink_events(cursor=sink_cursor)
        print(f"Loaded {num_sink_events} sink events")
    except MercuryError as exc:
        click.echo(f"Couldn't load sink events from Mercury")
        click.echo(repr(exc), err=True)


@load.command(name="retirements")
def db_load_retirements():
    """Load retirements into the DB"""
    retirement_date = get_latest_attr('retirement')
    num_retirements = load_retirements(from_date=retirement_date) # type: ignore[arg-type]
    click.echo(f"Loaded {num_retirements} retirements")


@load.command(name="associations")
def db_load_associations():
    """Load associations into the DB"""
    num_retirement_from_block = load_retirement_from_block()
    click.echo(f"Loaded {num_retirement_from_block} retirement-from-block associations")
    num_sink_statuses = load_sink_statuses()
    click.echo(f"Loaded {num_sink_statuses} sink status associations")

# MIGRATIONS

@cli.group()
def schema():
    """Database schema migration commands"""
    pass

@schema.command(name="current")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose mode")
def db_current_schema(verbose):
    """Display current database revision"""
    migrations.current(verbose)


@schema.command(name="upgrade")
@click.argument("revision", default="head")
def db_upgrade_schema(revision):
    """Upgrade to a later database revision"""
    migrations.upgrade(revision)


@schema.command(name="downgrade")
@click.argument("revision")
def db_downgrade_schema(revision):
    """Revert to a previous database revision. Specify "base" to reset the DB schema."""
    migrations.downgrade(revision)

# BACKUP

@cli.group()
def backup():
    """Database dump and restore commands"""
    pass


@backup.command(name="dump")
@click.argument("output_dir", type=click.Path(file_okay=False, dir_okay=True), required=True)
@click.option("-t", "--table", required=False, multiple=True, type=click.Choice(get_table_names()))
def db_dump_tables(output_dir, table: list[str]):
    """Dump the selected tables to ndjson files (default: all tables)"""
    tables = table  # ugly
    if not tables:
        tables = get_table_names()

    output = Path(output_dir)
    output.mkdir(exist_ok=True)
    for table_name in tables:
        file_path = output / f"{table_name}.ndjson"
        dump_table(db_model=table_name, output_path=file_path)
        click.echo(f"Wrote {table_name} to {file_path}")


@backup.command(name="restore")
@click.argument("input_dir", type=click.Path(file_okay=False, dir_okay=True), required=True)
@click.option("--replace", is_flag=True, help="Replace existing rows in tables with the backup")
@click.option("-t", "--table", required=False, multiple=True, help="The table name, see `dump`")
def db_restore_tables(input_dir, replace: bool, table: list[str]):
    """Restore the selected tables to the database (default: all files)"""
    selected_tables = table  # ugly
    input_dir = Path(input_dir)

    if selected_tables:
        for db_model in TABLE_LOADING_ORDER:
            table_name = db_model.__table__.name # type: ignore
            if table_name in selected_tables:
                dump_file = input_dir / f"{table_name}.ndjson"
                restore_table(dump_file, replace=replace)
    else:
        restore_all_tables(input_dir, replace=replace)

    