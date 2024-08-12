# Changelog

## [0.7.2](https://github.com/stellarcarbon/sc-audit/compare/v0.7.1...v0.7.2) (2024-08-12)


### Bug Fixes

* specify paging_token as BigInt for postgres compatibility ([e0f0152](https://github.com/stellarcarbon/sc-audit/commit/e0f015222bff7ebebf976b206f9ca6c772fc7e9a))

## [0.7.1](https://github.com/stellarcarbon/sc-audit/compare/v0.7.0...v0.7.1) (2024-08-10)


### Bug Fixes

* change HexBinary to LargeBinary for postgres compatibility ([f909554](https://github.com/stellarcarbon/sc-audit/commit/f9095541d12e24d08ae4fe8686158ab9ed3f2e05))

## [0.7.0](https://github.com/stellarcarbon/sc-audit/compare/v0.6.0...v0.7.0) (2024-07-30)


### Features

* add carbon stats view ([c5c3f7d](https://github.com/stellarcarbon/sc-audit/commit/c5c3f7d212f2934636155e312404339a3669837a))

## [0.6.0](https://github.com/stellarcarbon/sc-audit/compare/v0.5.0...v0.6.0) (2024-07-26)


### Features

* add test-prefixed tables ([7a38e1e](https://github.com/stellarcarbon/sc-audit/commit/7a38e1e6683bca7bd0fffeabe25b7c84ce38d8c8))
* configure db tables with optional prefix ([8b56a9e](https://github.com/stellarcarbon/sc-audit/commit/8b56a9e0cd70adaad7f368fe53ee15017c36e46c))

## [0.5.0](https://github.com/stellarcarbon/sc-audit/compare/v0.4.0...v0.5.0) (2024-07-16)


### Features

* add retirement view ([dc19448](https://github.com/stellarcarbon/sc-audit/commit/dc194482ae82fd7296d01968ef330042603a3586))
* add vcs project to retirement detail ([e662e50](https://github.com/stellarcarbon/sc-audit/commit/e662e5086bcf2915463c1a9476138d8be2b987f6))
* **cli:** add view retirements command ([4ac3234](https://github.com/stellarcarbon/sc-audit/commit/4ac32341940c3ddd5381f11b53eadbdc951ef0e7))


### Dependencies

* fix minor vulnerability ([1b50984](https://github.com/stellarcarbon/sc-audit/commit/1b50984923de2bdcb5ddff978f9bc7b39e7007e5))

## [0.4.0](https://github.com/stellarcarbon/sc-audit/compare/v0.3.1...v0.4.0) (2024-07-10)


### Features

* add pagination parameters to sink view ([ab92983](https://github.com/stellarcarbon/sc-audit/commit/ab929833488a7da1fb68ea4173413210125c97dc))
* add single sink tx getter ([bf5b6df](https://github.com/stellarcarbon/sc-audit/commit/bf5b6df8a4e91bcee28af420d8db315401343052))


### Bug Fixes

* default to desc order in sink view ([ed0bd79](https://github.com/stellarcarbon/sc-audit/commit/ed0bd797b264705231a9d7ed73f8ef90bfa390d0))
* omit empty statuses from outerjoin ([ca94ce8](https://github.com/stellarcarbon/sc-audit/commit/ca94ce839e1e0e9b69f7bf280d65ea474d2e923e))

## [0.3.1](https://github.com/stellarcarbon/sc-audit/compare/v0.3.0...v0.3.1) (2024-07-04)


### Dependencies

* upgrade stellar-sdk version ([8a2e595](https://github.com/stellarcarbon/sc-audit/commit/8a2e595b92bcc3fa079adbb7e391f10958abe30e))

## [0.3.0](https://github.com/stellarcarbon/sc-audit/compare/v0.2.0...v0.3.0) (2024-06-28)


### Features

* **backup:** download DB table dumps from GitHub ([94cef47](https://github.com/stellarcarbon/sc-audit/commit/94cef4725327683f1886b38749162bd14feef86d))
* **backup:** dump DB tables to newline-delimited json files ([ce04285](https://github.com/stellarcarbon/sc-audit/commit/ce042854179f2faa7d37c39460e3dffc67f9668e))
* **backup:** restore DB tables from newline-delimited json files ([a7ada25](https://github.com/stellarcarbon/sc-audit/commit/a7ada250702bb428fb6da6432d08f8c41e4d32a3))
* **cli:** add backup dump command ([88a4f67](https://github.com/stellarcarbon/sc-audit/commit/88a4f67809af73677d9a7272da0006c7de85e2ef))
* **cli:** add backup restore command ([80ad2f9](https://github.com/stellarcarbon/sc-audit/commit/80ad2f921fa5cfb36e67efbc1291a22b13ba05a4))
* **cli:** add bootstrap from dumps to catch-up command ([861e917](https://github.com/stellarcarbon/sc-audit/commit/861e917a6915fe4360024a2cb6a24baae168b3b7))
* load carbon distribution outflows ([a0f58bf](https://github.com/stellarcarbon/sc-audit/commit/a0f58bf436d7f503bff112473d48eef39a70d5c1))


### Dependencies

* update dependencies ([9068349](https://github.com/stellarcarbon/sc-audit/commit/9068349aecb93b7177f96c9b83e2824fa09e44c3))

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
