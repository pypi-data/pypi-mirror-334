import json
import typer
from rich import print_json
from rich.table import Table
from rich.console import Console
from lambdo.inc.helpers import get_response


app = typer.Typer(invoke_without_command=True, add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    """
    Retrieves a list of available images by region from the Lambda Labs Public Cloud API.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/images | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/images").json()["data"]
    if debug:
        print_json(json.dumps(resp), indent=2)
    # Create and add columns to filesystem table
    table = Table()
    table.add_column("ID", justify="right")
    table.add_column("Name", justify="right")
    table.add_column("Version", justify="right")
    table.add_column("Architecture", justify="right")
    table.add_column("Region", justify="right")

    # Iterate over all filesystems and add each row to the table
    for image in resp:
        this_id = image["id"]
        name = image["name"]
        version = image["version"]
        architecture = image["architecture"]
        region_name = image["region"]["name"]

        table.add_row(
            this_id,
            name,
            version,
            architecture,
            region_name,
        )

    # Create and print table
    console = Console()
    console.print(table)
