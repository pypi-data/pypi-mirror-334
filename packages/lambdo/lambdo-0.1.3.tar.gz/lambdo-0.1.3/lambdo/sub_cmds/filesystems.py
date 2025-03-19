import json
import typer
from rich import print_json
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated
from lambdo.inc.helpers import get_response, post_request, delete_request


app = typer.Typer(invoke_without_command=True, add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    """
    Display persistent storage filesystems from the Lambda Labs Public Cloud API.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems").json()[
        "data"
    ]
    if debug:
        print_json(json.dumps(resp), indent=2)
    # Create and add columns to filesystem table
    table = Table()
    table.add_column("ID", justify="right")
    table.add_column("Name", justify="right")
    table.add_column("Mount Point", justify="right")
    table.add_column("Created", justify="right")
    table.add_column("Created By", justify="right")
    table.add_column("In Use", justify="right")
    table.add_column("Region Name", justify="right")
    table.add_column("Description", justify="right")

    # Iterate over all filesystems and add each row to the table
    for fs in resp:
        this_id = fs["id"]
        name = fs["name"]
        mount_point = fs["mount_point"]
        created = fs["created"]
        created_by = fs["created_by"]["email"]
        in_use = "True" if fs["is_in_use"] else "False"
        region_name = fs["region"]["name"]
        region_desc = fs["region"]["description"]

        table.add_row(
            this_id,
            name,
            mount_point,
            created,
            created_by,
            in_use,
            region_name,
            region_desc,
        )

    # Create and print table
    console = Console()
    console.print(table)


@app.command("create", help="Create a filesystem")
def create_filesystem(
    name: Annotated[str, typer.Option(help="The name of the filesystem")],
    region: Annotated[str, typer.Option(help="The region name")],
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    data = {"name": name, "region": region}
    #
    resp = post_request(
        url="https://cloud.lambdalabs.com/api/v1/filesystems",
        data=data,
    )
    if resp.status_code == 200:
        typer.echo(f"File system was created with id={resp.json()['data']['id']}")
    if debug:
        typer.echo(json.dumps(resp.json(), indent=2))


@app.command("delete", help="Delete a filesystem")
def delete_filesystem(
    id: Annotated[
        str, typer.Option(help="The id of the filesystem you want to delete")
    ],
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    resp = delete_request(url=f"https://cloud.lambdalabs.com/api/v1/filesystems/{id}")
    if resp.status_code == 200:
        typer.echo("The filesystem was deleted successfully")
    else:
        typer.Exit(code=1)
    if debug:
        typer.echo(json.dumps(resp.json(), indent=2))
