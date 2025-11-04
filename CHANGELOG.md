# Changelog

## [0.12.1](https://github.com/stellarcarbon/sc-audit/compare/v0.12.0...v0.12.1) (2025-11-04)


### Dependencies

* bump pygithub to v2.8.x ([1e4acd7](https://github.com/stellarcarbon/sc-audit/commit/1e4acd7bd7e4000a663b5a013151c629763c59c3))

## [0.12.0](https://github.com/stellarcarbon/sc-audit/compare/v0.11.0...v0.12.0) (2025-08-27)


### Features

* **view:** add contract call filter ([c8c6503](https://github.com/stellarcarbon/sc-audit/commit/c8c65037be6c57cfa158f9fc4ecc7223dab0771e))

## [0.11.0](https://github.com/stellarcarbon/sc-audit/compare/v0.10.6...v0.11.0) (2025-08-27)


### Features

* **Flow:** Provide an alternative for Mercury events using Obsrvr Flow extracted invocations ([#28](https://github.com/stellarcarbon/sc-audit/issues/28)) ([342fe54](https://github.com/stellarcarbon/sc-audit/commit/342fe5496d858c62e6a0cb617c577a9b2b2db6dc))
* separate latest classic tx and SinkContract tx on the basis of contract_id ([64c41ff](https://github.com/stellarcarbon/sc-audit/commit/64c41ff86d97c6b792bf41ecc00307b010481057))


### Bug Fixes

* only bind event listener to sqlite backends ([837aed2](https://github.com/stellarcarbon/sc-audit/commit/837aed286f79f87cab036d07533592127a97e54a))

## [0.10.6](https://github.com/stellarcarbon/sc-audit/compare/v0.10.5...v0.10.6) (2025-08-15)


### Bug Fixes

* **sources:** increase Verra asset search timeout to 10s ([8831a74](https://github.com/stellarcarbon/sc-audit/commit/8831a74f79c99826e431d8e7259336ca87e7521e))


### Dependencies

* bump to latest compatible ([7ce18a9](https://github.com/stellarcarbon/sc-audit/commit/7ce18a9c3209f668593cbaa52822f4c1acfb32a2))

## [0.10.5](https://github.com/stellarcarbon/sc-audit/compare/v0.10.4...v0.10.5) (2025-07-18)


### Bug Fixes

* **migrations:** apply branch label in new revision ([8dbd146](https://github.com/stellarcarbon/sc-audit/commit/8dbd1462e1f6b2f1d88a0c5d57379110d0d43126))
* **migrations:** wrap `context.get_context()` in a function ([8e7c48a](https://github.com/stellarcarbon/sc-audit/commit/8e7c48aae8b029eb3bca8604de2cb3360e6350fb))

## [0.10.4](https://github.com/stellarcarbon/sc-audit/compare/v0.10.3...v0.10.4) (2025-06-27)


### Bug Fixes

* **pagination:** refactor sink status queries to improve pagination predictability ([67c9756](https://github.com/stellarcarbon/sc-audit/commit/67c975654f0707158837ea2ac923cb7c3370153c))
* **SinkStatus:** make finalized filters perfect negations of each other ([2691c3e](https://github.com/stellarcarbon/sc-audit/commit/2691c3ee9c105cf4003901f8d526eac691d8fdd9))
* **SinkStatus:** raise on empty sink status ([74e77a4](https://github.com/stellarcarbon/sc-audit/commit/74e77a42efef903c59f1530854afab9373fb7898))


### Performance Improvements

* order by paging_token rather than created_at ([60da22a](https://github.com/stellarcarbon/sc-audit/commit/60da22a103d1da54fab9c8222413af014168a04a))

## [0.10.3](https://github.com/stellarcarbon/sc-audit/compare/v0.10.2...v0.10.3) (2025-06-23)


### Bug Fixes

* **Mercury:** update RETROSHADES_MD5 ([31eae99](https://github.com/stellarcarbon/sc-audit/commit/31eae990b9fbee713ed23759a27a9946fc9ce310))


### Dependencies

* bump pygithub to v2.6.x; poetry update ([17a58b4](https://github.com/stellarcarbon/sc-audit/commit/17a58b4354a47dc61b3f6e4ef0be1c43222494f0))

## [0.10.2](https://github.com/stellarcarbon/sc-audit/compare/v0.10.1...v0.10.2) (2025-06-18)


### Bug Fixes

* prefix foreign key constraints ([d1b4cb6](https://github.com/stellarcarbon/sc-audit/commit/d1b4cb6b1c8e14e3bd7d2aed855ac8d53a59e3a1))

## [0.10.1](https://github.com/stellarcarbon/sc-audit/compare/v0.10.0...v0.10.1) (2025-06-16)


### Bug Fixes

* unpack load_sink_events return value ([de10e1c](https://github.com/stellarcarbon/sc-audit/commit/de10e1ce138c885307e90fad36468c7c37ca0ac9))

## [0.10.0](https://github.com/stellarcarbon/sc-audit/compare/v0.9.4...v0.10.0) (2025-06-14)


### Features

* Ingest SinkEvents as SinkingTxs ([#21](https://github.com/stellarcarbon/sc-audit/issues/21)) ([f87fb81](https://github.com/stellarcarbon/sc-audit/commit/f87fb817520c8eca5d91de38d6b6a3c12adbc2ae))


### Documentation

* **cli:** update for v0.10 ([d9abb32](https://github.com/stellarcarbon/sc-audit/commit/d9abb321ba32bb362b31c6386eb27a910aadc96e))
* pre-commit install ([3ceb239](https://github.com/stellarcarbon/sc-audit/commit/3ceb23914f805f0e0f0f71b50f60777ead671c3c))

## [0.9.4](https://github.com/stellarcarbon/sc-audit/compare/v0.9.3...v0.9.4) (2025-05-16)


### Bug Fixes

* stop fetching from github on every import ([0db220e](https://github.com/stellarcarbon/sc-audit/commit/0db220e46de2f28ff76d05ff942f4a71a9aea273))


### Dependencies

* fix critical vulnerability ([5fe39b4](https://github.com/stellarcarbon/sc-audit/commit/5fe39b485343fef5be49a4b6f4e2d1524033fb2b))

## [0.9.3](https://github.com/stellarcarbon/sc-audit/compare/v0.9.2...v0.9.3) (2025-05-02)


### Bug Fixes

* prevent the table prefix from being applied multiple times ([877fcbb](https://github.com/stellarcarbon/sc-audit/commit/877fcbbdd452b2a04765f4e37af60bfb99c2bf35))

## [0.9.2](https://github.com/stellarcarbon/sc-audit/compare/v0.9.1...v0.9.2) (2025-04-18)


### Bug Fixes

* validate retirement.serial_number ([9233f57](https://github.com/stellarcarbon/sc-audit/commit/9233f57dccb84f1d16c58c9cc1b467207801ec50))

## [0.9.1](https://github.com/stellarcarbon/sc-audit/compare/v0.9.0...v0.9.1) (2025-03-28)


### Dependencies

* fix major vulnerability ([02d2a3d](https://github.com/stellarcarbon/sc-audit/commit/02d2a3db537c3b5f0cfd6a3334f3e7c8a6a10740))

## [0.9.0](https://github.com/stellarcarbon/sc-audit/compare/v0.8.2...v0.9.0) (2024-12-30)


### Features

* **backup:** exclude testnet data from DB dumps ([befc5da](https://github.com/stellarcarbon/sc-audit/commit/befc5da402de068d29f2c3e717f80427f50110a7))


### Bug Fixes

* don't fetch next payments in tests ([df102f1](https://github.com/stellarcarbon/sc-audit/commit/df102f122ebc07315a3c2b336fef50efca4478ae))

## [0.8.2](https://github.com/stellarcarbon/sc-audit/compare/v0.8.1...v0.8.2) (2024-09-09)


### Bug Fixes

* stricter filtering of sinking transactions ([4d79d99](https://github.com/stellarcarbon/sc-audit/commit/4d79d99bb87fdff96042ed32d70b52c76892ad89))

## [0.8.1](https://github.com/stellarcarbon/sc-audit/compare/v0.8.0...v0.8.1) (2024-09-09)


### Bug Fixes

* prefix all foreign key column references ([4f446fa](https://github.com/stellarcarbon/sc-audit/commit/4f446fad891083b1e0e55d10ba7b5597903991e6))

## [0.8.0](https://github.com/stellarcarbon/sc-audit/compare/v0.7.4...v0.8.0) (2024-08-28)


### Features

* provide initial VCS project ([9adb635](https://github.com/stellarcarbon/sc-audit/commit/9adb6358383ac365dac0693a164826bffefabdfe))

## [0.7.4](https://github.com/stellarcarbon/sc-audit/compare/v0.7.3...v0.7.4) (2024-08-12)


### Bug Fixes

* replace total with sum+coalesce ([dddeea1](https://github.com/stellarcarbon/sc-audit/commit/dddeea10318ad6d2f7575f5217c95d3456c26670))

## [0.7.3](https://github.com/stellarcarbon/sc-audit/compare/v0.7.2...v0.7.3) (2024-08-12)


### Miscellaneous Chores

* release 0.7.3 ([8a529dd](https://github.com/stellarcarbon/sc-audit/commit/8a529dd5d0e4cfcc1676319469937f3a22cfa709))

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
