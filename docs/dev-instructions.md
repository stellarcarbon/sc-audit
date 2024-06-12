# Development

Instructions for developers who may want to contribute to this project.

## Prerequisites

- Supported Python installation (v3.12+)
- [Python Poetry](https://python-poetry.org/docs/)

## Set-up

After cloning this git repository, install the dependencies with:

```bash
poetry install
```

You also need to install the git hooks that are configured for this repo:

```bash
pre-commit install
```

## Release management

We use [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) messages to help keep the changelog up-to-date. The git hook you've installed above will enforce this lightweight specification for any commits you'll make. These commit messages are used to automatically update the changelog during the release process.

[Release Please](https://github.com/googleapis/release-please) keeps track of all commits to the main branch since the last release. It creates a Release PR that appropriately increments the version number and adds entries to the changelog. Once the Release PR is merged, a GitHub release is created, and a new version of the sc-audit package is published to PyPI.
