import time
from typer.testing import CliRunner

from lambdo.sub_cmds.filesystems import app

runner = CliRunner()


def test_filesystem():
    time.sleep(1.5)
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0
