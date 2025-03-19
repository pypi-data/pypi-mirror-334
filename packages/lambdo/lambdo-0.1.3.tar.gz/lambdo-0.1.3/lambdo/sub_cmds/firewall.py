import json
import typer
from rich import print_json
from rich.table import Table
from rich.console import Console
from lambdo.inc.helpers import get_response, put_request


app = typer.Typer(invoke_without_command=True, add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    """
    Retrieves a list of your firewall rules from the Lambda Labs Public Cloud API.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/firewall-rules | jq .
    resp = get_response(
        url="https://cloud.lambdalabs.com/api/v1/firewall-rules"
    ).json()["data"]
    if debug:
        print_json(json.dumps(resp), indent=2)
    # Create and add columns to filesystem table
    table = Table()
    table.add_column("Protocol", justify="right")
    table.add_column("Port Range", justify="right")
    table.add_column("Source Network", justify="right")
    table.add_column("Description", justify="right")

    # Iterate over all filesystems and add each row to the table
    for rule in resp:
        protocol = rule["protocol"]
        port_range = (
            ",".join(str(p) for p in rule["port_range"])
            if "port_range" in rule.keys()
            else None
        )
        source_network = rule["source_network"]
        description = rule["description"]

        table.add_row(
            protocol,
            port_range,
            source_network,
            description,
        )

    # Create and print table
    console = Console()
    console.print(table)


@app.command("update", help="Overwrites the inbound firewall rules currently active")
def update_firewall_rules(
    protocol: str | None = typer.Option(None, "--protocol", "-p"),
    port_range: str | None = typer.Option(
        None, "--port-range", "-r", help="Range of ports allowed"
    ),
    source_network: str | None = typer.Option(
        None, "--source-net", "-s", help="Source network allowed"
    ),
    description: str | None = typer.Option(
        None, "--description", help="Description of the firewall rule"
    ),
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    updated_rule = {
        "protocol": protocol,
        "port_range": [int(i) for i in port_range.split(",")],
        "source_network": source_network,
        "description": description,
    }

    get_current_rules = get_response(
        url="https://cloud.lambdalabs.com/api/v1/firewall-rules"
    ).json()["data"]

    # Verify if the rule that is being applied exists already
    if updated_rule in get_current_rules:
        typer.echo("This rule already exists")
        return
    elif updated_rule["port_range"] in [
        d["port_range"] for d in get_current_rules if "port_range" in d.keys()
    ] and updated_rule["source_network"] in [
        d["source_network"] for d in get_current_rules
    ]:
        typer.echo(
            "This rule already exists with the given port range and source network"
        )
        return
    # Append the new rule to the current rules
    get_current_rules.append(updated_rule)

    data = {"data": get_current_rules}

    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/firewall-rules | jq .
    resp = put_request(
        url="https://cloud.lambdalabs.com/api/v1/firewall-rules", data=data
    )
    if resp.status_code == 200:
        typer.echo("Firewall updated was accepted")
    if debug:
        print_json(json.dumps(resp.json()), indent=2)
