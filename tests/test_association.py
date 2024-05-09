
import pytest
from sqlalchemy import select

from sc_audit.db_schema.association import RetirementFromBlock
from sc_audit.loader import minted_blocks, retirement_from_block
from sc_audit.loader.utils import VcsSerialNumber
from tests.data_fixtures.retirements import get_retirements
from tests.db_fixtures import new_session, vcs_project
from tests.test_mint import mock_http


class TestRetirementFromBlock:
    def test_cover_retirement_block_start(self, mock_session_with_blocks):
        retirement = get_retirements()[0]
        serial_number = VcsSerialNumber.from_str(retirement.serial_number)
        retirement.vcu_amount = 1
        serial_number.block_start = 449402277
        serial_number.block_end = 449402277
        retirement.serial_number = serial_number.to_str()

        with mock_session_with_blocks.begin() as session:
            rfbs = retirement_from_block.cover_retirement(session, retirement)
            assert len(rfbs) == 1
            rfb: retirement_from_block.RetirementFromBlock = rfbs[0]
            assert rfb.retirement_id == retirement.certificate_id
            assert rfb.vcu_amount == retirement.vcu_amount
            session.add(rfb)
            session.flush()
            assert rfb.block.block_start == serial_number.block_start
            assert rfb.block.block_end != serial_number.block_end

    def test_cover_retirement_block_end(self, mock_session_with_blocks):
        retirement = get_retirements()[0]
        serial_number = VcsSerialNumber.from_str(retirement.serial_number)
        retirement.vcu_amount = 2
        serial_number.block_start = 449402299
        serial_number.block_end = 449402300
        retirement.serial_number = serial_number.to_str()

        with mock_session_with_blocks.begin() as session:
            rfbs = retirement_from_block.cover_retirement(session, retirement)
            assert len(rfbs) == 1
            rfb: retirement_from_block.RetirementFromBlock = rfbs[0]
            assert rfb.retirement_id == retirement.certificate_id
            assert rfb.vcu_amount == retirement.vcu_amount
            session.add(rfb)
            session.flush()
            assert rfb.block.block_start != serial_number.block_start
            assert rfb.block.block_end == serial_number.block_end

    def test_cover_retirement_block_middle(self, mock_session_with_blocks):
        retirement = get_retirements()[0]
        serial_number = VcsSerialNumber.from_str(retirement.serial_number)
        retirement.vcu_amount = 3
        serial_number.block_start = 449402280
        serial_number.block_end = 449402282
        retirement.serial_number = serial_number.to_str()

        with mock_session_with_blocks.begin() as session:
            rfbs = retirement_from_block.cover_retirement(session, retirement)
            assert len(rfbs) == 1
            rfb: retirement_from_block.RetirementFromBlock = rfbs[0]
            assert rfb.retirement_id == retirement.certificate_id
            assert rfb.vcu_amount == retirement.vcu_amount
            session.add(rfb)
            session.flush()
            assert rfb.block.block_start != serial_number.block_start
            assert rfb.block.block_end != serial_number.block_end

    def test_cover_retirement_spans_two(self, mock_session_with_blocks):
        retirement = get_retirements()[0]
        serial_number = VcsSerialNumber.from_str(retirement.serial_number)
        retirement.vcu_amount = 24
        serial_number.block_start = 449402280
        serial_number.block_end = 449402303
        retirement.serial_number = serial_number.to_str()

        with mock_session_with_blocks.begin() as session:
            rfbs = retirement_from_block.cover_retirement(session, retirement)
            assert len(rfbs) == 2
            rfb_one, rfb_two = rfbs
            for rfb in rfbs:
                assert rfb.retirement_id == retirement.certificate_id
                
            assert rfb_one.vcu_amount == 21
            assert rfb_two.vcu_amount == 3
            session.add_all(rfbs)
            session.flush()
            assert rfb_one.block.block_start < serial_number.block_start < rfb_one.block.block_end
            assert rfb_two.block.block_start < serial_number.block_end < rfb_two.block.block_end

    def test_cover_retirement_spans_three(self, mock_session_with_blocks):
        retirement = get_retirements()[0]
        serial_number = VcsSerialNumber.from_str(retirement.serial_number)
        retirement.vcu_amount = 32
        serial_number.block_start = 449402289
        serial_number.block_end = 449402320
        retirement.serial_number = serial_number.to_str()

        with mock_session_with_blocks.begin() as session:
            rfbs = retirement_from_block.cover_retirement(session, retirement)
            assert len(rfbs) == 3
            rfb_one, rfb_two, rfb_three = rfbs
            for rfb in rfbs:
                assert rfb.retirement_id == retirement.certificate_id
                
            assert rfb_one.vcu_amount == 12
            assert rfb_two.vcu_amount == 16
            assert rfb_three.vcu_amount == 4
            session.add_all(rfbs)
            session.flush()
            assert rfb_one.block.block_start < serial_number.block_start < rfb_one.block.block_end
            assert rfb_two.vcu_amount == rfb_two.block.size
            assert rfb_three.block.block_start < serial_number.block_end < rfb_three.block.block_end

    def test_cover_retirement_overspent(self, mock_session_with_blocks):
        retirements = get_retirements()
        with mock_session_with_blocks.begin() as session:
            session.add_all(retirement_from_block.cover_retirement(session, retirements[0]))
            session.add_all(retirement_from_block.cover_retirement(session, retirements[1]))

            with pytest.raises(retirement_from_block.BlockOverspent):
                retirement_from_block.cover_retirement(session, retirements[1])

    def test_cover_retirement_uncovered(self, mock_session_with_blocks):
        # craft a retirement that extends beyond a known block range
        retirement = get_retirements()[0]
        serial_number = VcsSerialNumber.from_str(retirement.serial_number)
        retirement.vcu_amount = 7
        serial_number.block_start = 449402320
        serial_number.block_end = 449402326
        retirement.serial_number = serial_number.to_str()

        with mock_session_with_blocks.begin() as session:
            with pytest.raises(retirement_from_block.CoveringBlockMissing):
                retirement_from_block.cover_retirement(session, retirement)

    def test_load_retirement_from_block(self, mock_session_with_blocks):
        with mock_session_with_blocks.begin() as session:
            retirement_from_block.load_retirement_from_block()

        with mock_session_with_blocks.begin() as session:
            rfbs = session.scalars(select(RetirementFromBlock)).all()
            assert len(rfbs) == 11
            rfb_total_amount = sum(rfb.vcu_amount for rfb in rfbs)
            retirement_total_amount = sum(ret.vcu_amount for ret in get_retirements())
            assert rfb_total_amount == retirement_total_amount

    def test_load_rfb_overspent(self, mock_session_with_blocks):
        duplicate_retirement = get_retirements()[0]
        duplicate_retirement.certificate_id = 0
        with mock_session_with_blocks.begin() as session:
            session.add(duplicate_retirement)
        
        with pytest.raises(retirement_from_block.BlockOverspent):
            retirement_from_block.load_retirement_from_block()


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(minted_blocks, 'Session', new_session)
    monkeypatch.setattr(retirement_from_block, 'Session', new_session)
    return new_session

@pytest.fixture
def mock_session_with_blocks(mock_http, mock_session, vcs_project):
    with mock_session.begin() as session:
        session.add(vcs_project)
        session.add_all(get_retirements())

    minted_blocks.load_minted_blocks()
    return mock_session
