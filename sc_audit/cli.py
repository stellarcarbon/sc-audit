"""
SC Audit command line interface.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

import click

from sc_audit import migrations
from sc_audit.loader.__main__ import catch_up_from_sources
from sc_audit.loader.get_latest import get_latest_attr
from sc_audit.loader.minted_blocks import load_minted_blocks
from sc_audit.loader.retirement_from_block import load_retirement_from_block
from sc_audit.loader.retirements import load_retirements
from sc_audit.loader.sink_status import load_sink_statuses
from sc_audit.loader.sinking_txs import load_sinking_txs
from sc_audit.views.inventory import view_inventory
from sc_audit.views.sink_status import view_sinking_txs
from sc_audit.views.utils import format_df


@click.group()
@click.version_option(package_name="sc_audit")
def cli():
    """CLI for Stellarcarbon Audit tool"""
    pass

@cli.command(name="catch-up")
def db_catch_up():
    """Let the DB catch up with the data sources"""
    # TODO: bootstrap by restoring DB dump
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
@click.option("--omit-empty", is_flag=True, default=False, help="Don't show empty minted blocks")
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

@load.command(name="minted-blocks")
def db_load_minted_blocks():
    """Load minted blocks into the DB"""
    mint_cursor = get_latest_attr('mint_tx')
    num_minting_txs = load_minted_blocks(cursor=mint_cursor) # type: ignore
    click.echo(f"Loaded {num_minting_txs} minted blocks")

@load.command(name="sinking-txs")
def db_load_sinking_txs():
    """Load sinking transactions into the DB"""
    sink_cursor = get_latest_attr('sink_tx')
    num_sinking_txs = load_sinking_txs(cursor=sink_cursor) # type: ignore
    click.echo(f"Loaded {num_sinking_txs} sinking transactions")

@load.command(name="retirements")
def db_load_retirements():
    """Load retirements into the DB"""
    retirement_date = get_latest_attr('retirement')
    num_retirements = load_retirements(from_date=retirement_date) # type: ignore
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
