import datetime as dt

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.exc as orm_exc

from sc_audit.db_schema import *

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
ScBase.metadata.create_all(engine)
Session = sessionmaker(engine)


@pytest.fixture
def vcs_project() -> VcsProject:
    return VcsProject(
        id=1360, 
        name="Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region", 
        category="Agriculture Forestry and Other Land Use", 
        protocol="VM0015", 
        additional_certifications="CCB-Gold", 
        region="Latin America", 
        country="Peru"
    )

@pytest.fixture
def first_block(vcs_project: VcsProject) -> MintedBlock:
    shash = "016023e64fefb1304a73aeab0877db032d7feceff25e390c00cf15d3fc4cfb79"
    txhash = "61efb636bd2fb32efbd9a6379cd3ba55a96fb200ef3c523568168374d0aa0980"
    serial_number = "8040-449402275-449402275-VCU-042-MER-PE-14-1360-01072013-30062014-1"
    mint_timestamp = dt.datetime(2021, 11, 20, 13, 6, 51, tzinfo=dt.timezone.utc)
    return MintedBlock(
        serial_hash=shash, 
        transaction_hash=txhash, 
        created_at=mint_timestamp, 
        vcs_project_id=vcs_project.id,
        serial_number=serial_number, 
        block_size=1, 
        sub_account_id=11273,
        sub_account_name="CARBON Pool | stellarcarbon.io", 
        vintage_start=dt.date(2011, 1, 1), 
        vintage_end=dt.date(2014, 1, 1)
    )

class TestMint:
    def test_insert_block(self, vcs_project: VcsProject, first_block: MintedBlock):
        assert first_block.vcs_project_id == vcs_project.id

        with Session.begin() as session:
            session.add(vcs_project)
            session.add(first_block)

        # after commit, the objects are no longer bound to the session
        with pytest.raises(orm_exc.DetachedInstanceError):
            first_block.vcs_project

    def test_get_block(self, first_block: MintedBlock, vcs_project: VcsProject):
        with Session.begin() as session:
            found_block = session.get_one(MintedBlock, first_block.serial_hash)
            assert found_block.transaction_hash == first_block.transaction_hash
            assert found_block.vcs_project.id == vcs_project.id

        