# Changelog

## 0.2.0 (2024-06-21)


### Features

* build docker image ([c2f153a](https://github.com/stellarcarbon/sc-audit/commit/c2f153ab37fb71985c1c3489c9df94382c746eab))
* publish releases to ghcr.io ([24c90e8](https://github.com/stellarcarbon/sc-audit/commit/24c90e8f15729faf1413628be41afa04ef408dd7))


### Bug Fixes

* let the db be mounted in a pre-defined volume ([095b95e](https://github.com/stellarcarbon/sc-audit/commit/095b95e95b2623c17958f18c288a4161bdb332ff))


### Documentation

* document python usage ([0708e5a](https://github.com/stellarcarbon/sc-audit/commit/0708e5a987e8ca015f56bb29ad8662cb86384571))
* initial changelog ([942786d](https://github.com/stellarcarbon/sc-audit/commit/942786d0aac86cda07daa01151c91ba369e1e140))
* move progress into docs ([8c180d3](https://github.com/stellarcarbon/sc-audit/commit/8c180d3090174c097da0284ea249c04ec3c6c9e8))
* unified readme ([b0ecc0a](https://github.com/stellarcarbon/sc-audit/commit/b0ecc0a3e15cb40083693a65ff0e4ea4761c7fd8))

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
