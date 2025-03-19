import time
from typer.testing import CliRunner

from lambdo.sub_cmds.ssh_keys import app

runner = CliRunner()


def test_ssh_keys():
    time.sleep(1.5)
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0


def test_ssh_keys_add():
    time.sleep(1.5)
    result = runner.invoke(app, args=["add", "--help"])
    assert result.exit_code == 0


def test_ssh_keys_delete():
    time.sleep(1.5)
    result = runner.invoke(app, args=["delete", "--help"])
    assert result.exit_code == 0
