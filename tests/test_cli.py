from typer.testing import CliRunner
from unittest.mock import patch, AsyncMock
from app.cli import app

runner = CliRunner()


def test_upload_file_not_found():
    result = runner.invoke(app, ["upload", "nonexistent.csv"])
    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_process_file_not_found():
    result = runner.invoke(app, ["process", "test-id", "nonexistent.csv"])
    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_results_not_found():
    with patch("app.cli.storage") as mock_storage:
        mock_storage.get_file_record = AsyncMock(return_value=None)
        result = runner.invoke(app, ["results", "nonexistent-id"])

    assert result.exit_code == 1
    assert "not found" in result.stdout
