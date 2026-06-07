"""Tests for the progress tracker CLI."""
import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.progress_tracker import (
    init_progress,
    load_progress,
    save_progress,
    render_dashboard,
    generate_report,
    PHASES,
    VALID_STATUSES,
)


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory with progress.json."""
    project_root = str(tmp_path)
    data = init_progress(project_root, "test-project")
    return project_root, data


class TestInitProgress:
    """Test progress initialization."""

    def test_init_creates_file(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        assert data["project"] == "test-project"
        assert data["total_phases"] == 37
        assert data["completed_phases"] == 0
        assert len(data["phases"]) == 37

    def test_init_all_phases_pending(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        for phase_id, phase_data in data["phases"].items():
            assert phase_data["status"] == "pending"


class TestLoadSaveProgress:
    """Test loading and saving progress."""

    def test_save_and_load(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        loaded = load_progress(project_root)
        assert loaded is not None
        assert loaded["project"] == "test-project"
        assert loaded["total_phases"] == 37

    def test_load_nonexistent(self, tmp_path):
        loaded = load_progress(str(tmp_path))
        assert loaded is None


class TestDashboard:
    """Test dashboard rendering."""

    def test_render_dashboard(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        dashboard = render_dashboard(data)
        assert "HYBRID HARNESS" in dashboard
        assert "test-project" in dashboard
        assert "0/37" in dashboard
        assert "Foundation" in dashboard

    def test_render_dashboard_with_progress(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        # Mark first phase as completed
        data["phases"]["00-orchestrator"]["status"] = "completed"
        data["phases"]["00-orchestrator"]["completed_at"] = "2026-01-01T00:00:00Z"
        data["completed_phases"] = 1
        save_progress(project_root, data)

        dashboard = render_dashboard(data)
        assert "1/37" in dashboard


class TestReport:
    """Test report generation."""

    def test_generate_report(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        report = generate_report(data)
        assert "# Workflow Progress Report" in report
        assert "test-project" in report
        assert "0/37" in report

    def test_report_with_completed_phases(self, tmp_path):
        project_root = str(tmp_path)
        data = init_progress(project_root, "test-project")
        data["phases"]["00-orchestrator"]["status"] = "completed"
        data["phases"]["01-ba-requirements"]["status"] = "in_progress"
        data["completed_phases"] = 1

        report = generate_report(data)
        assert "completed" in report
        assert "in_progress" in report


class TestPhaseValidation:
    """Test that all expected phases exist."""

    def test_all_phases_present(self):
        phase_ids = [p["id"] for p in PHASES]
        assert "00-orchestrator" in phase_ids
        assert "35-devils-advocate" in phase_ids
        assert len(PHASES) == 37

    def test_valid_statuses(self):
        assert "pending" in VALID_STATUSES
        assert "in_progress" in VALID_STATUSES
        assert "completed" in VALID_STATUSES
        assert "blocked" in VALID_STATUSES
        assert "skipped" in VALID_STATUSES
