from pathlib import Path

from alembic.config import Config
from alembic import command


package_root = Path(__file__).parent.parent
alembic_config = Config(package_root / "alembic.ini")


def current(verbose=False):
    command.current(alembic_config, verbose=verbose)


def upgrade(revision="head"):
    command.upgrade(alembic_config, revision)


def downgrade(revision):
    command.downgrade(alembic_config, revision)
