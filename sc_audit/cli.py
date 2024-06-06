
import click

from sc_audit import migrations


@click.group()
def cli():
    """CLI for Stellarcarbon Audit tool"""
    pass

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
