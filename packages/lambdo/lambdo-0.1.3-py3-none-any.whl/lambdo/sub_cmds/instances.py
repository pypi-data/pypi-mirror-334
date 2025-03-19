import json
import typer
from requests import Response
from rich import print_json
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated
from lambdo.inc.helpers import get_response, post_request


app = typer.Typer(invoke_without_command=True, add_completion=False)


def create_and_print_instance_table(resp: Response):
    table = Table()
    table.add_column("ID")
    table.add_column("Status Code")

    this_id = ",".join(n for n in resp.json()["data"]["instance_ids"])
    status_code = str(resp.status_code)

    table.add_row(this_id, status_code)

    # Print Table
    console = Console()
    console.print(table)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    """
    Display instances from the Lambda Labs Public Cloud API.

    By default, prints all active instances.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances").json()[
        "data"
    ]
    if debug:
        print_json(json.dumps(resp), indent=2)

    if len(resp) == 0:
        typer.echo("There are no instances running...")
        return

    table = Table()
    table.add_column("ID", justify="right")
    table.add_column("Status", justify="right")
    table.add_column("Location", justify="right")
    table.add_column("Description", justify="right")
    table.add_column("Price Per Hour", justify="right")
    table.add_column("Hostname", justify="right")
    table.add_column("Public IP", justify="right")
    table.add_column("Jupyter Labs URL", justify="right")

    for inst in resp:
        inst_id = inst["id"]
        status = inst["status"]
        location = inst["region"]["name"]
        description = inst["instance_type"]["description"]
        price = f'${inst["instance_type"]["price_cents_per_hour"] / 100:.2f}'
        hostname = inst["hostname"] if "hostname" in inst.keys() else ""
        public_ip = inst["ip"]
        jupyter_url = inst["jupyter_url"]

        table.add_row(
            inst_id,
            status,
            location,
            description,
            price,
            hostname,
            public_ip,
            jupyter_url,
        )

    # Print Table
    console = Console()
    console.print(table)


@app.command("detail", help="Retrieve the details of an instance")
def get_instance_details(
    inst_id: Annotated[str, typer.Option(help="The id of the instance")],
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances/INSTANCE-ID | jq .
    resp = get_response(
        url=f"https://cloud.lambdalabs.com/api/v1/instances/{inst_id}"
    ).json()["data"]
    if debug:
        print_json(json.dumps(resp), indent=2)

    table = Table()
    table.add_column("ID", justify="right")
    table.add_column("Status", justify="right")
    table.add_column("SSH Key Names", justify="right")
    table.add_column("File System Names", justify="right")
    table.add_column("Location", justify="right")
    table.add_column("GPU", justify="right")
    table.add_column("Description", justify="right")
    table.add_column("Price Per Hour", justify="right")
    table.add_column("Hostname", justify="right")

    inst_id = resp["id"]
    status = resp["status"]
    ssh_key_name = ",".join(n for n in resp["ssh_key_names"])
    file_system_name = ",".join(n for n in resp["file_system_names"])
    location = resp["region"]["name"]
    name = resp["instance_type"]["name"]
    description = resp["instance_type"]["description"]
    price = f'${resp["instance_type"]["price_cents_per_hour"] / 100:.2f}'
    hostname = resp["hostname"] if "hostname" in resp.keys() else ""

    table.add_row(
        inst_id,
        status,
        ssh_key_name,
        file_system_name,
        location,
        name,
        description,
        price,
        hostname,
    )

    # Print Table
    console = Console()
    console.print(table)


@app.command("create", help="Create an instance")
def create_instance(
    region_name: Annotated[str, typer.Option(help="The region name")],
    instance_type_name: Annotated[str, typer.Option(help="The instance type name")],
    ssh_key_names: Annotated[list[str], typer.Option(help="The name of the ssh key")],
    filesystems: Annotated[list[str], typer.Option(help="The name of the filesystems")],
    quantity: Annotated[int, typer.Option(help="The quantity of instances")] = 1,
    name: Annotated[
        str | None, typer.Option(help="The custom name of the instance")
    ] = None,
    from_file: Annotated[
        str | None, typer.Option(help="Path to a file containing required parameters")
    ] = None,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    if from_file is not None:
        file = {"file": open(from_file)}
        # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/launch -d @request.json
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/launch",
            files=file,
        )
    else:
        data = {
            "region_name": region_name,
            "instance_type_name": instance_type_name,
            "ssh_key_names": ssh_key_names,
            "file_system_names": filesystems,
            "quantity": quantity,
            "name": name,
        }
        # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/launch -d @request.json
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/launch",
            data=data,
        )
    if debug:
        typer.echo(json.dumps(resp.json()["data"]["instance_ids"], indent=2))

    # Create generic table for create, restart, and delete
    create_and_print_instance_table(resp)


@app.command("restart", help="Restart instance(s)")
def restart_instances(
    inst_id: Annotated[
        list[str], typer.Option(help="The id of the instance(s) you want to restart")
    ],
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    data = {"instance_ids": inst_id}
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/restart -d @INSTANCE-IDS
    resp = post_request(
        url="https://cloud.lambdalabs.com/api/v1/instance-operations/restart", data=data
    )
    if debug:
        typer.echo(json.dumps(resp.json()["data"]["instance_ids"], indent=2))

    # Create generic table for create, restart, and delete
    create_and_print_instance_table(resp)


@app.command("delete", help="Delete instance(s)")
def delete_instances(
    inst_id: Annotated[
        list[str], typer.Option(help="The id of the instance(s) you want to delete")
    ],
    from_file: Annotated[
        str | None, typer.Option(help="Path to a file containing required parameters")
    ] = None,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/terminate -d @INSTANCE-IDS
    if from_file is not None:
        file = {"file": open(from_file)}
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/terminate",
            files=file,
        )
    else:
        data = {"instance_ids": inst_id}
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/terminate",
            data=data,
        )
    if debug:
        typer.echo(json.dumps(resp.json()["data"]["instance_ids"], indent=2))

    # Create generic table for create, restart, and delete
    create_and_print_instance_table(resp)
