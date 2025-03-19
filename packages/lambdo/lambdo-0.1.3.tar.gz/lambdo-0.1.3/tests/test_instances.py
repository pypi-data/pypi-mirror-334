import time
from typer.testing import CliRunner

from lambdo.sub_cmds.instances import app

runner = CliRunner()


def test_instances():
    time.sleep(1.5)
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0


def test_instances_create():
    time.sleep(1.5)
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0


def test_instances_delete():
    time.sleep(1.5)
    result = runner.invoke(app, ["delete", "--help"])
    assert result.exit_code == 0


def test_instances_detail():
    time.sleep(1.5)
    result = runner.invoke(app, ["detail", "--help"])
    assert result.exit_code == 0


def test_instances_restart():
    time.sleep(1.5)
    result = runner.invoke(app, ["restart", "--help"])
    assert result.exit_code == 0
