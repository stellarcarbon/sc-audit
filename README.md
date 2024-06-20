# Stellarcarbon Audit DB

Core database with monitoring and audit functionality.

This is a stand-alone tool that can be used to monitor and audit Stellarcarbon accounts through a command-line interface. We recommend the use of sc-audit through Docker for users who don't want to manage their own Python installation. If you're already running a recent version of Python, installation of the Python package is likely the most convenient option.

Programmatic access to sc-audit and its data is possible in several ways. To integrate it with your Python project, simply include the sc-audit package as a dependency. Other environments are able to use the CLI for basic commands, and can either use the filesystem or a connection to its SQLite database to obtain the data and do further processing.

## Docker usage

Start by pulling the latest published image from ghcr.io:

```bash
docker pull ghcr.io/stellarcarbon/sc-audit
```

This Docker image is intended for single-command usage. It will not keep running a process, and exits as soon as it is done. Mount its data volume locally to persist the database, and run the containers with `--rm` to avoid the litter of stopped containers.

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
