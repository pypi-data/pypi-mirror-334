from pathlib import Path

# tests/test_cli.py
import pytest
from click.testing import CliRunner
from simple_hosting_capacity.cli import run_hosting_capacity
from simple_hosting_capacity.cli import build_plots

BASE_TEST_PATH = Path(__file__).parent
OPENDSS_PATH = BASE_TEST_PATH / "data" / "Master.dss"
TEST_DUMP = BASE_TEST_PATH / "test_dump"
HOSTING_CAPACITY_FILE = TEST_DUMP / "hosting_capacity.csv"


@pytest.fixture
def runner():
    return CliRunner()


def test_run_hosting_capacity_help(runner):
    if not TEST_DUMP.exists():
        TEST_DUMP.mkdir()

    result = runner.invoke(run_hosting_capacity, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_run_hosting_capacity_missing_model(runner):
    result = runner.invoke(run_hosting_capacity)
    assert result.exit_code != 0
    assert "Missing argument 'MODEL'" in result.output


def test_run_hosting_capacity_valid_args(runner, tmp_path):
    result = runner.invoke(
        run_hosting_capacity,
        [
            str(OPENDSS_PATH),
            "-l",
            "100",
            "-h",
            "200",
            "-f",
            "1",
            "-p",
            "1",
            "-a",
            "1",
            "-m",
            "1",
            "-t",
            "1",
            "-e",
            str(HOSTING_CAPACITY_FILE),
        ],
    )
    assert result.exit_code == 0
    assert TEST_DUMP.exists()


def test_build_plots_help(runner):
    result = runner.invoke(build_plots, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_build_plots_missing_model(runner):
    result = runner.invoke(build_plots)
    assert result.exit_code != 0
    assert "Missing argument 'MODEL'" in result.output


def test_build_plots_valid_args(runner):
    voltage_distance_file = TEST_DUMP / "voltage_distance.html"
    heatmap_file = TEST_DUMP / "heatmap.html"
    result = runner.invoke(
        build_plots,
        [
            str(OPENDSS_PATH),
            "-p",
            str(HOSTING_CAPACITY_FILE),
            "-l",
            "True",
            "-v",
            str(voltage_distance_file),
            "-h",
            str(heatmap_file),
        ],
    )
    assert result.exit_code == 0
    assert voltage_distance_file.exists()
    assert heatmap_file.exists()
