import time
from typer.testing import CliRunner

from lambdo.sub_cmds.instance_types import app

runner = CliRunner()

# Sleep times were needed because it looks like I'm getting throttled by Lambda Labs...


def test_instance_types():
    time.sleep(1.5)
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0


def test_instance_types_available():
    time.sleep(1.5)
    result = runner.invoke(app, ["--available"])
    assert result.exit_code == 0


def test_instance_types_unavailable():
    time.sleep(1.5)
    result = runner.invoke(app, ["--unavailable"])
    assert result.exit_code == 0


def test_instance_types_by_gpu_name_gnu_long():
    time.sleep(1.5)
    result = runner.invoke(app, ["gpu", "--name", "gpu_1x_gh200"])
    assert result.exit_code == 0


def test_instance_types_by_gpu_name_short():
    time.sleep(1.5)
    result = runner.invoke(app, ["gpu", "-n", "gpu_1x_gh200"])
    assert result.exit_code == 0


def test_instance_types_by_location_gnu_long():
    time.sleep(1.5)
    result = runner.invoke(app, ["location", "--name", "us-east-1"])
    assert result.exit_code == 0


def test_instance_types_by_location_short():
    time.sleep(1.5)
    result = runner.invoke(app, ["location", "-n", "us-east-1"])
    assert result.exit_code == 0


def test_instance_types_by_location_city():
    time.sleep(1.5)
    result = runner.invoke(app, ["location", "-n", "virginia"])
    assert result.exit_code == 0
