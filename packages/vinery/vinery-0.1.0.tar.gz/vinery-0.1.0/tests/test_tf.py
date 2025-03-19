import pytest
import subprocess
from unittest.mock import patch, MagicMock
from vinery.tf import load_runners, SUPPORTED_RUNNERS, tf


def test_load_runners_returns_all_runners_if_all_runners_exist():
    # All supported runners must exist in the test environment!
    assert load_runners() == SUPPORTED_RUNNERS


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for controlled command execution."""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_update_file():
    """Mock update_file function to prevent actual file writing."""
    with patch("vinery.tf.update_file") as mock_update:
        yield mock_update


@pytest.fixture
def mock_echo():
    """Mock echo function to suppress output in tests."""
    with patch("vinery.tf.echo") as mock_echo_fn:
        yield mock_echo_fn


def test_tf_success(mock_subprocess_run, mock_update_file, mock_echo):
    """Test tf() when the command runs successfully."""
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout=b"Success output")

    result = tf("my_plan", "my_runner", "my_cmd", "my_path")

    assert result == 0, "Expected return code 0 for success"
    mock_subprocess_run.assert_called_once()
    mock_echo.assert_any_call("Command 'my_runner my_cmd' for plan 'my_plan' was successful!", log_level="SUCCESS")


def test_tf_failure(mock_subprocess_run, mock_update_file, mock_echo):
    """Test tf() when the command fails."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "terraform apply")

    result = tf("my_plan", "my_runner", "my_cmd", "my_path")

    assert result == 1, "Expected return code 1 for failure"
    mock_subprocess_run.assert_called_once()
    mock_echo.assert_any_call("Command 'my_runner my_cmd' failed for plan my_plan!", log_level="ERROR")


def test_tf_save_output(mock_subprocess_run, mock_update_file, mock_echo):
    """#Test tf() when save_output=True."""
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout=b"Saved output")

    result = tf("my_plan", "my_runner", "my_cmd", "my_path", save_output=True)

    assert result == 0, "Expected return code 0 when saving output"
    mock_update_file.assert_called_once_with(
        "my_cmd_my_plan.log", ["Saved output"], dir="output"
    )
    mock_echo.assert_any_call("Command 'my_runner my_cmd' for plan 'my_plan' was successful!", log_level="SUCCESS")
