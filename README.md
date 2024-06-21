# Stellarcarbon Audit DB

Core database with monitoring and audit functionality.

This is a stand-alone tool that can be used to monitor and audit Stellarcarbon accounts through a command-line interface. We recommend the use of sc-audit through Docker for users who don't want to manage their own Python installation. If you're already running a recent version of Python, installation of the Python package is likely the most convenient option.

Programmatic access to sc-audit and its data is possible in several ways. To integrate it with your Python project, simply include the sc-audit package as a dependency. Other environments are able to use the CLI for basic commands, and can either use the filesystem or a connection to its SQLite database to obtain the data and do further processing.

## Docker usage

Start by pulling the latest published image from ghcr.io:

```bash
docker pull ghcr.io/stellarcarbon/sc-audit
```

This Docker image is intended for single-command usage. It will not keep a process running, and exits as soon as it is done. Mount its data volume locally to persist the database, and run the containers with `--rm` to avoid the litter of stopped containers.

You'll want to let the database catch up with its data sources at the start of each usage session:

```bash
docker run --rm -v sc-data:/opt/data ghcr.io/stellarcarbon/sc-audit catch-up
```

The `--help` flag provides interactive documentation for the CLI. It may also be used in combination with (sub-)commands to get information about their parameters.

```bash
$ docker run --rm -v sc-data:/opt/data ghcr.io/stellarcarbon/sc-audit --help

Connecting to database sqlite+pysqlite:////opt/data/sc-audit.sqlite3...
Usage: sc-audit [OPTIONS] COMMAND [ARGS]...

  CLI for Stellarcarbon Audit tool

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  catch-up  Let the DB catch up with the data sources
  load      Load data from their original sources
  schema    Database schema migration commands
  view      View the state of Stellarcarbon assets and transactions
```

Since the `docker run` prefix is fairly long, you might find it convenient to declare a shell alias that lets you run commands as if the CLI was running outside of a container:

```bash
alias sc-audit="docker run --rm -v sc-data:/opt/data ghcr.io/stellarcarbon/sc-audit"
```

Refer to your OS or shell documentation to learn how to persist this alias across shell sessions. After configuring the alias, you'll be able to use `sc-audit` as if you'd installed it through Python. Keep reading to learn more about the provided commands.

## Python usage

### Installation

Install the sc-audit package and CLI from PyPI:

```bash
pip install sc-audit
```

Please note that if you install sc-audit into a virtualenv (recommended), the `sc-audit` script will only be available when this virtualenv is activated.

### Setup

The database needs to be initialized with the latest version of the DB schema. We use Alembic to manage migrations. Before using sc-audit, ensure that your local DB is created with the latest schema definitions:

```bash
sc-audit schema upgrade
```

To achieve the same from your Python code, you may do:

```python
from sc_audit import migrations

migrations.upgrade(revision="head")
```

After upgrading sc-audit to a newer version, you may need to also need to upgrade the DB schema. Repeat the above instructions to run any new migrations. The provided Docker image already takes care of running DB migrations, so there's no need to run them manually.

### Loading data

The easiest way to get a consistent view on Stellarcarbon's inventory and sinking transactions is to use the `catch-up` command, before using any of the view commands. This will load the latest data from all available sources into the DB. It is idempotent, so the command can be run repeatedly without problems. There is, however, the possibility that you'll run into rate limits for requests to external sources if the command is used very frequently.

Use the catch-up command every time you want to inspect the current state of Stellarcarbon's accounts:

```bash
sc-audit catch-up
```

The `load` commands aren't needed for normal usage, but they are provided for special use cases. It is possible to monitor, for instance, only retirements or sinking transactions, if you wish to do so.

```text
Usage: sc-audit load [OPTIONS] COMMAND [ARGS]...

  Load data from their original sources

Options:
  --help  Show this message and exit.

Commands:
  associations   Load associations into the DB
  minted-blocks  Load minted blocks into the DB
  retirements    Load retirements into the DB
  sinking-txs    Load sinking transactions into the DB
```

The Python API for loading data is contained in the `sc_audit.loader` module. Take a look at the `sc_audit.loader.__main__.catch_up_from_sources` function for inspiration on how to load only new records into the DB.

### Viewing data

The `inventory` and `sink` views each combine different types of source data. The inventory is (re)constructed by taking all blocks of credits that have been minted by Stellarcarbon, and by deducting the credits that have already been retired from their remaining credits.

```text
Usage: sc-audit view inventory [OPTIONS]

  View Stellarcarbon's current or historical inventory of eco-credits

Options:
  -f, --format [df|csv|json]  The output format for this view  [default: df]
  --omit-empty                Don't show empty minted blocks
  --until-date [%Y-%m-%d]     Reconstruct the inventory on the given date
  --help                      Show this message and exit.
```

The default output format is a human-readable table view. It is currently wide and will eventually become long as well. We therefore recommend to use a screen pager without line wrapping to comfortably view the inventory table:

```bash
sc-audit view inventory | less -S
```

Both csv and json are available as machine-readable output formats. Common usage is to either pipe the output to another command or to redirect it to a file:

```bash
sc-audit view inventory -f csv > sc-inventory-$(date +"%Y-%m-%d").csv
```

The Python API is located at `sc_audit.views.inventory` and returns the inventory table as a Pandas DataFrame:

```python
def view_inventory(omit_empty: bool = False, until_date: dt.date | None = None) -> pd.DataFrame
```

The sink view combines sinking transactions with their associated retirements (stored as `SinkStatus` objects). It can be filtered in several ways.

```text
Usage: sc-audit view sink [OPTIONS]

  View sinking transactions and their retirement status

Options:
  -f, --format [df|csv|json]  The output format for this view  [default: df]
  --funder TEXT               Only show transactions for the given funder
                              address
  --recipient TEXT            Only show transactions for the given recipient
                              address
  --from-date [%Y-%m-%d]      Filter transactions that happened on or after
                              the given date
  --before-date [%Y-%m-%d]    Filter transactions that happened before the
                              given date
  --finalized BOOLEAN         Filter by retirement status
  --help                      Show this message and exit.
```

As with the inventory view, use horizontal scrolling:

```bash
sc-audit view sink | less -S
```

Or redirect the machine readable output to a file:

```bash
sc-audit view sink -f json > sc-sink-$(date +"%Y-%m-%d").json
```

The Python API is located at `sc_audit.views.sink_status` and returns the sinking transactions table as a Pandas DataFrame:

```python
def view_sinking_txs(
        for_funder: str | None = None,
        for_recipient: str | None = None, 
        from_date: dt.date | None = None,
        before_date: dt.date | None = None,
        finalized: bool | None = None,
) -> pd.DataFrame
```

### Configuration

There isn't much to configure in sc-audit. Two variables can be overriden by environment variables.

| env variable     | description               |
|------------------|---------------------------|
| `SC_DBAPI_URL`   | default: `sqlite+pysqlite:///{get_default_db_path()}`<br>The default value places an SQLite DB file in the working dir or in a subdir of the home dir. |
| `SC_HORIZON_URL` | default: `https://horizon.stellar.org`<br>Set this value to a Horizon instance with full history to be able to do a fresh load. |

## Development

Instructions for developers who may want to contribute to this project.

### Prerequisites

- Supported Python installation (v3.12+)
- [Python Poetry](https://python-poetry.org/docs/)

### Set-up

After cloning this git repository, install the dependencies with:

```bash
poetry install
```

You also need to install the git hooks that are configured for this repo:

```bash
pre-commit install
```

### Release management

We use [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) messages to help keep the changelog up-to-date. The git hook you've installed above will enforce this lightweight specification for any commits you'll make. These commit messages are used to automatically update the changelog during the release process.

[Release Please](https://github.com/googleapis/release-please) keeps track of all commits to the main branch since the last release. It creates a Release PR that appropriately increments the version number and adds entries to the changelog. Once the Release PR is merged, a GitHub release is created, and a new version of the sc-audit package is published to PyPI. A Docker image is simultaneously built and published to ghrc.io.
