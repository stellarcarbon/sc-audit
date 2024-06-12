# Changelog

## 0.1.1 (2024-06-10)

Initial release, lacking docs and DB dump and restore functionality.

### Features

* Database schema and filling from Horizon and the Verra Registry
* Database logic to compute inventory and pending retirements views
* Command-line interface `sc-audit`, with commands to:
  * set up and migrate the database schema
  * load data from their original sources
  * let the DB catch up with the data sources
  * view the state of Stellarcarbon assets and transactions

### Documentation

* `sc-audit` CLI interactive command docs
