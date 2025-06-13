
import pytest

from sc_audit.loader import impact_projects
from tests.db_fixtures import new_session


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    return new_session


class TestImpactProjectsLoader:
    def test_load_projects_idempotent(self, mock_session):
        load_one = impact_projects.load_impact_projects()
        assert load_one == 1
        load_two = impact_projects.load_impact_projects()
        assert load_two == 0
        load_tri = impact_projects.load_impact_projects()
        assert load_tri == 0
