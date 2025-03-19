import os
import json
import typer
from pathlib import Path


# Points to the user's home directory, e.g. /home/username or C:\Users\Username
HOME_DIR = Path.home()

# Subfolder for our CLI config
LAMBDO_CONFIG_DIR = HOME_DIR / ".lambdo"

# Our actual config file: ~/.lambdo/config
LAMBDO_CONFIG_PATH = LAMBDO_CONFIG_DIR / "config.json"


def load_config() -> dict:
    """
    Load the configuration from ~/.lambdo/config (JSON).
    Returns an empty dict if the file does not exist or is invalid.
    """
    if not LAMBDO_CONFIG_PATH.exists():
        return {}
    try:
        with open(LAMBDO_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # If file is corrupted or unreadable, return empty
        return {}


def save_config(data: dict):
    """
    Save the given dict `data` as JSON to ~/.lambdo/config.
    Creates the directory if it doesn't exist.
    """
    LAMBDO_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LAMBDO_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


try:
    settings = load_config()
    api_key = settings.get("API_KEY", "put-your-api-key-here")
    ssh_path = settings.get("SSH_PATH", "put-your-ssh-path-here")
    if os.getenv("API_KEY") and os.getenv("SSH_PATH"):
        api_key = os.getenv("API_KEY")
        ssh_path = os.getenv("SSH_PATH")
    elif api_key == "put-your-api-key-here" or ssh_path == "put-your-ssh-path-here":
        api_key = typer.prompt("Enter your Lambda Labs API Key")
        ssh_path = typer.prompt("Enter your ssh key path")
        # Write the variables provided to the local .env file
        # Update our config dictionary
        if "~/" in ssh_path:
            ssh_path = os.path.expanduser(ssh_path)
        # Write user-provided variables to correlating keys
        settings["API_KEY"] = api_key
        settings["SSH_PATH"] = ssh_path

        # Save back to file
        save_config(settings)
        typer.echo(f"Configuration has been saved to {LAMBDO_CONFIG_PATH}")

except KeyError:
    typer.echo("Uh oh, It looks like you haven't properly setup lambdo...")
    typer.echo("    Run `lambdo setup` to configure your local parameters")
    exit()
