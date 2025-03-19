import json
import typer
import requests
from requests import Response, HTTPError
from typing import Optional
from rich import print_json
from lambdo.inc.settings import api_key


# A useful link to Lambda Labs Cloud API Docs: https://cloud.lambdalabs.com/api/v1/docs
def get_response(url: str) -> Response:
    """
    Helper function to get a response
    """
    try:
        response = requests.get(url=url, auth=(api_key, ""))
        response.raise_for_status()
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)

    return response


def post_request(
    url: str,
    data: Optional[dict | list[dict] | None] = None,
    files: Optional[dict | list | None] = None,
) -> Response:
    """
    Helper function to post a request
    """
    headers = {"Content-Type": "application/json"}
    try:
        if data is not None:
            data = json.dumps(data)
            response = requests.post(
                url=url, auth=(api_key, ""), data=data, headers=headers
            )
        elif files is not None:
            response = requests.post(
                url=url, auth=(api_key, ""), files=files, headers=headers
            )
        else:
            response = requests.post(url=url, auth=(api_key, ""), headers=headers)
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)
    try:
        response.raise_for_status()
    except HTTPError:
        typer.echo(
            "There was an issue with your request. See the below error for more details."
        )

    return response


def delete_request(url: str) -> Response:
    """
    Helper function to delete a resource
    """
    try:
        response = requests.delete(url=url, auth=(api_key, ""))
        response.raise_for_status()
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)

    return response


def put_request(
    url: str,
    data: Optional[dict | list[dict] | None] = None,
    files: Optional[dict | list | None] = None,
) -> Response:
    """
    Helper function to put a request
    """
    headers = {"Content-Type": "application/json"}
    try:
        if data is not None:
            data = json.dumps(data)
            response = requests.put(
                url=url, auth=(api_key, ""), data=data, headers=headers
            )
        elif files is not None:
            response = requests.put(
                url=url, auth=(api_key, ""), files=files, headers=headers
            )
        else:
            response = requests.put(url=url, auth=(api_key, ""), headers=headers)
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)
    try:
        response.raise_for_status()
    except HTTPError:
        typer.echo(
            "There was an issue with your request. See the below error for more details or use the --debug option."
        )
        print_json(json.dumps(response.json(), indent=2))

    return response
