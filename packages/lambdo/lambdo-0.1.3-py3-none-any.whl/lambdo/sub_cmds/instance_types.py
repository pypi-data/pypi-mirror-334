import json
import typer
from rich import print_json
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated
from lambdo.inc.helpers import get_response


app = typer.Typer(invoke_without_command=True, add_completion=False)


def create_instance_types_table(
    inst: dict | list, available: bool = False, unavailable: bool = False
) -> Table:
    """
    Create a rich table object that populates the instance types data from Lambda Labs
    """
    table = Table()
    table.add_column("GPU", justify="right")
    table.add_column("Locations", justify="right")
    table.add_column("Description", justify="right")
    table.add_column("Price Per Hour", justify="right")
    table.add_column("VCPUs", justify="right")
    table.add_column("Memory", justify="right")
    table.add_column("# of GPUs", justify="right")

    if isinstance(inst, dict):
        # Get locations list
        available_locations = inst["regions_with_capacity_available"]
        # Combine any locations found
        locations = (
            ",".join(n["name"] for n in available_locations)
            if len(available_locations) >= 1
            else None
        )

        gpu_dict = inst["instance_type"]

        # Assign all row items
        name = gpu_dict["name"]
        description = gpu_dict["description"]
        price = f'${gpu_dict["price_cents_per_hour"] / 100:.2f}'
        vcpus = str(gpu_dict["specs"]["vcpus"])
        vram = gpu_dict["specs"]["memory_gib"]
        vram = f"{vram}GB" if len(str(vram)) <= 3 else f"{vram / 1000:.2f}TB"
        num_gpus = str(gpu_dict["specs"]["gpus"])

        table.add_row(name, locations, description, price, vcpus, vram, num_gpus)
    elif isinstance(inst, list):
        for i in inst:
            # Get locations list
            available_locations = i["regions_with_capacity_available"]
            # Combine any locations found
            locations = (
                ",".join(n["name"] for n in available_locations)
                if len(available_locations) >= 1
                else None
            )

            gpu_dict = i["instance_type"]

            # Assign all row items
            name = gpu_dict["name"]
            description = gpu_dict["description"]
            price = f'${gpu_dict["price_cents_per_hour"] / 100:.2f}'
            vcpus = str(gpu_dict["specs"]["vcpus"])
            vram = gpu_dict["specs"]["memory_gib"]
            vram = f"{vram}GB" if len(str(vram)) <= 3 else f"{vram / 1000:.2f}TB"
            num_gpus = str(gpu_dict["specs"]["gpus"])

            # Add table row based on available or unavailable
            if available and locations is None:
                continue
            elif unavailable and locations is not None:
                continue
            else:
                table.add_row(
                    name, locations, description, price, vcpus, vram, num_gpus
                )

            # table.add_row(name, locations, description, price, vcpus, vram, num_gpus)
    else:
        typer.Exit(1)

    return table


def print_table(table: Table):
    # Print Table
    console = Console()
    console.print(table)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    available: bool = typer.Option(
        False, "--available", help="Show only available instance types."
    ),
    unavailable: bool = typer.Option(
        False, "--unavailable", help="Show only unavailable instance types."
    ),
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    """
    Display instance types from the Lambda Labs Public Cloud API.

    By default, prints all instance types. Optionally, filter to only available or
    unavailable instance types using --available or --unavailable.
    """
    # If a subcommand (like gpu or location) is invoked, skip this callback.
    if ctx.invoked_subcommand is not None:
        return

    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(
        url="https://cloud.lambdalabs.com/api/v1/instance-types"
    ).json()["data"]

    if debug:
        print_json(json.dumps(resp), indent=2)

    # Make response iterable to make it easier for parsing
    resp = [resp[inst] for inst in resp]

    # Create and print table
    table = create_instance_types_table(resp, available, unavailable)
    print_table(table)


@app.command("gpu", help="Search for a particular GPU by name")
def get_gpu(
    name: Annotated[
        str, typer.Option("--name", "-n", help="Provide the name of the gpu")
    ],
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    try:
        resp = get_response(
            url="https://cloud.lambdalabs.com/api/v1/instance-types"
        ).json()["data"][name]
        if debug:
            print_json(json.dumps(resp), indent=2)
        # Create and print instance table
        table = create_instance_types_table(resp)
        print_table(table)

    except KeyError:
        typer.echo("There is not a GPU with that name...")
        typer.Exit(1)


@app.command("location", help="Search for GPUs by location")
def get_location(
    name: Annotated[str, typer.Option("--name", "-n", help="Search by location")],
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(
        url="https://cloud.lambdalabs.com/api/v1/instance-types"
    ).json()["data"]
    if debug:
        print_json(json.dumps(resp), indent=2)

    # Find any instance that has the provided location listed
    find_by_location = [
        loc
        for inst in resp
        for loc in resp[inst]["regions_with_capacity_available"]
        if name.lower() in loc["description"].lower() or name.lower() in loc["name"]
    ]
    if find_by_location:
        # If there were any, then get a list of the instances to iterate over
        available_instance = [
            resp[inst]
            for inst in resp
            if find_by_location[0] in resp[inst]["regions_with_capacity_available"]
        ]
        # Create and print instance table
        table = create_instance_types_table(available_instance)
        print_table(table)
    else:
        typer.echo("There are currently no instances available...")
