import os
import typer
from typing_extensions import Annotated
from lambdo.inc.settings import load_config, save_config, LAMBDO_CONFIG_PATH


app = typer.Typer(invoke_without_command=True, add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    api_key: Annotated[str, typer.Option(prompt="Enter your Lambda Labs API Key")],
    ssh_path: Annotated[str, typer.Option(prompt="Enter your ssh key path")],
):
    """
    Setup command for lambdo that helps store your API Key and ssh path
    """
    if ctx.invoked_subcommand is not None:
        return

    settings = load_config()
    # Update our config dictionary
    if "~/" in ssh_path:
        ssh_path = os.path.expanduser(ssh_path)
    # Write user-provided variables to correlating keys
    settings["API_KEY"] = api_key
    settings["SSH_PATH"] = ssh_path

    # Save back to file
    save_config(settings)
    typer.echo(f"Configuration has been saved to {LAMBDO_CONFIG_PATH}")
