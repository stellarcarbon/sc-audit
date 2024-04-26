# sc-audit

Core database with monitoring and audit functionality

## SCF#25

Follow along with our progress:

[Deliverable 1]

    Database schema and filling from Horizon and the Verra Registry

- [x] set up a local database
- [ ] load minting transactions from Horizon
- [x] load sinking transactions from Horizon
- [x] load retirements from Verra
- [ ] test coverage

[Deliverable 2]

    Database logic to compute inventory and pending retirements views

- [ ] fill m2m tables
- [ ] view the status of sinking transactions
- [ ] view the current inventory
- [ ] test coverage

[Deliverable 3]

    CLI, packaging, and containerization

- [ ] Python packaging
- [ ] Dockerfile
- [ ] command line interface
  - [ ] fill the database
  - [ ] table view inventory
  - [ ] table view retirements
- [ ] documentation

[Deliverable 4]

    Database dump and restore tool

- [ ] dump core tables
- [ ] restore dumps
- [ ] catch up from live sources
- [ ] fresh load
- [ ] test coverage
