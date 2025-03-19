import typer
from lambdo.sub_cmds import (
    filesystems,
    firewall,
    images,
    instances,
    instance_types,
    setup,
    ssh_keys,
)


app = typer.Typer(
    help="Lambdo is a CLI tool that utilizes the Lambda GPU Cloud Public APIs",
    no_args_is_help=True,
)
app.add_typer(
    filesystems.app,
    name="filesystems",
    help="Manage your persistent storage filesystems",
)
app.add_typer(firewall.app, name="firewall", help="List and update your firewall rules")
app.add_typer(images.app, name="images", help="List available images")
app.add_typer(
    instances.app, name="instances", help="Manage your Lambda GPU Cloud instances"
)
app.add_typer(
    instance_types.app,
    name="instance-types",
    help="List the instance types offered by Lambda GPU Cloud",
)
app.add_typer(
    setup.app, name="setup", help="Setup Lambdo with your API KEY and SSH path"
)
app.add_typer(ssh_keys.app, name="ssh-keys", help="Manage SSH Keys for your instances")


def main():
    app()


if __name__ == "__main__":
    main()
