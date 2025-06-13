from decimal import Decimal

import pytest
from sqlalchemy import func, select

from sc_audit.db_schema.association import RetirementFromBlock, SinkStatus
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader import impact_projects, minted_blocks, retirement_from_block, sink_status
from sc_audit.loader import sinking_txs as sink_loader
from sc_audit.loader.utils import VcsSerialNumber
from tests.data_fixtures.retirements import get_retirements
from tests.db_fixtures import new_session
from tests.test_mint import mock_http as mock_mint_http
from tests.test_sink import mock_http as mock_sink_http


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


class TestSinkStatus:
    def test_create_sink_status_one(self, mock_session_with_sink_txs):
        retirement = get_retirements()[0]
        with mock_session_with_sink_txs.begin() as session:
            sink_statuses = sink_status.create_sink_statuses(session, retirement)
            assert len(sink_statuses) == 1
            status = sink_statuses[0]
            assert status.sinking_tx_hash == retirement.tx_hashes_from_details[0]
            assert status.certificate_id == retirement.certificate_id
            assert status.amount_filled == retirement.vcu_amount
            assert status.finalized is True

    def test_create_sink_status_two(self, mock_session_with_sink_txs):
        retirement = get_retirements()[10]
        with mock_session_with_sink_txs.begin() as session:
            sink_statuses = sink_status.create_sink_statuses(session, retirement)
            assert len(sink_statuses) == 2
            status_one, status_two = sink_statuses
            for i, status in enumerate([status_one, status_two]):
                assert status.sinking_tx_hash == retirement.tx_hashes_from_details[i]
                assert status.certificate_id == retirement.certificate_id
                assert status.amount_filled == status.sinking_transaction.carbon_amount
                assert status.finalized is True

    def test_create_sink_status_more(self, mock_session_with_sink_txs):
        retirement = get_retirements()[8]
        with mock_session_with_sink_txs.begin() as session:
            sink_statuses = sink_status.create_sink_statuses(session, retirement)
            assert len(sink_statuses) == 7
            for i, status in enumerate(sink_statuses):
                assert status.sinking_tx_hash == retirement.tx_hashes_from_details[i]
                assert status.certificate_id == retirement.certificate_id
                assert status.amount_filled == status.sinking_transaction.carbon_amount
                assert status.finalized is True

    def test_create_sink_status_pending(self, mock_session_with_sink_txs):
        # construct a retirement that partially fills a sink tx (filling in minimal fields)
        retirement = get_retirements()[0]
        retirement.retirement_details = "stellarcarbon.io 20dbafdc604fc1a48eafc4ce0df2b6151dfa5a5241c307f811a99ce4ddf2fb7f"
        retirement.vcu_amount = 3
        with mock_session_with_sink_txs.begin() as session:
            sink_statuses = sink_status.create_sink_statuses(session, retirement)
            assert len(sink_statuses) == 1
            status = sink_statuses[0]
            assert status.sinking_tx_hash == retirement.tx_hashes_from_details[0]
            assert status.certificate_id == retirement.certificate_id
            assert status.amount_filled == retirement.vcu_amount
            assert status.finalized is False

            # check sink tx amount filled and amount remaining
            sink_tx = status.sinking_transaction
            assert sink_tx.total_filled == retirement.vcu_amount
            assert sink_tx.carbon_amount - sink_tx.total_filled == Decimal("0.015")

    def test_load_sink_statuses(self, mock_session_with_sink_txs):
        sink_status.load_sink_statuses()
        with mock_session_with_sink_txs.begin() as session:
            sss = session.scalars(select(SinkStatus)).all()
            assert len(sss) == 18
            ss_total_amount = sum(ss.amount_filled for ss in sss)
            retirement_total_amount = sum(ret.vcu_amount for ret in get_retirements())
            assert ss_total_amount == retirement_total_amount

            q_finalized_txs = (
                select(func.sum(SinkingTx.carbon_amount))
                .join(SinkStatus)
                .where(SinkStatus.finalized == True)
            )
            finalized_tx_total_carbon = session.scalar(q_finalized_txs)
            assert finalized_tx_total_carbon == ss_total_amount

    def test_load_sink_statuses_idempotent(self, mock_session_with_sink_txs):
        sink_status.load_sink_statuses()
        sink_status.load_sink_statuses()
        with mock_session_with_sink_txs.begin() as session:
            sss = session.scalars(select(SinkStatus)).all()
            assert len(sss) == 18
            ss_total_amount = sum(ss.amount_filled for ss in sss)
            assert ss_total_amount == Decimal("23")


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    monkeypatch.setattr(minted_blocks, 'Session', new_session)
    monkeypatch.setattr(retirement_from_block, 'Session', new_session)
    monkeypatch.setattr(sink_loader, 'Session', new_session)
    monkeypatch.setattr(sink_status, 'Session', new_session)
    impact_projects.load_impact_projects()
    return new_session

@pytest.fixture
def mock_session_with_blocks(mock_mint_http, mock_session):
    with mock_session.begin() as session:
        session.add_all(get_retirements())

    minted_blocks.load_minted_blocks()
    return mock_session

@pytest.fixture
def mock_session_with_sink_txs(mock_sink_http, mock_session_with_blocks):
    sink_loader.load_sinking_txs(cursor=999)
    return mock_session_with_blocks
