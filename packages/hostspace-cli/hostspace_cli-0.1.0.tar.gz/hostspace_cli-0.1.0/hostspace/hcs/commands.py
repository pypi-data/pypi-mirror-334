"""Container Service (HCS) commands for HostSpace CLI."""
import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

from hostspace.utils.api import api_client, APIError

hcs_app = typer.Typer(help="Manage Container Service (HCS) resources")
console = Console()

@hcs_app.command()
def app_list():
    """List all container applications."""
    try:
        apps = api_client.get("/hcs/apps")
        table = Table(title="Container Applications")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Region", style="blue")
        table.add_column("Replicas", style="magenta")

        for app in apps.get("items", []):
            table.add_row(
                str(app.get("id")),
                app.get("name"),
                app.get("status"),
                app.get("region"),
                str(app.get("replicas", 1))
            )
        console.print(table)
    except APIError as e:
        console.print(f"[red]Error listing applications: {str(e)}[/red]")
        raise typer.Exit(1)

@hcs_app.command()
def app_deploy(
    name: str = typer.Option(..., "--name", "-n", help="Application name"),
    image: str = typer.Option(..., "--image", "-i", help="Container image"),
    region: str = typer.Option(..., "--region", "-r", help="Region to deploy in"),
    replicas: int = typer.Option(1, "--replicas", help="Number of replicas"),
    env: list[str] = typer.Option([], "--env", "-e", help="Environment variables (KEY=VALUE)"),
    port: int = typer.Option(None, "--port", "-p", help="Container port to expose"),
):
    """Deploy a new container application."""
    try:
        env_dict = {}
        for env_var in env:
            key, value = env_var.split("=", 1)
            env_dict[key] = value

        data = {
            "name": name,
            "image": image,
            "region": region,
            "replicas": replicas,
            "env": env_dict,
        }
        if port:
            data["port"] = port

        with console.status("[bold green]Deploying application..."):
            response = api_client.post("/hcs/apps", data)
            console.print("[green]Successfully deployed application![/green]")
            console.print(f"Application ID: {response.get('id')}")
    except APIError as e:
        console.print(f"[red]Error deploying application: {str(e)}[/red]")
        raise typer.Exit(1)

@hcs_app.command()
def app_logs(
    app_id: str = typer.Argument(..., help="ID of the application"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
    tail: int = typer.Option(100, "--tail", "-n", help="Number of lines to show"),
):
    """Get logs for a container application."""
    try:
        params = {"tail": tail}
        if follow:
            with Live(Spinner("dots"), refresh_per_second=10):
                while True:
                    logs = api_client.get(f"/hcs/apps/{app_id}/logs", params=params)
                    console.print(logs.get("output", ""))
        else:
            logs = api_client.get(f"/hcs/apps/{app_id}/logs", params=params)
            console.print(logs.get("output", ""))
    except APIError as e:
        console.print(f"[red]Error getting logs: {str(e)}[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped following logs[/yellow]")

@hcs_app.command()
def app_delete(
    app_id: str = typer.Argument(..., help="ID of the application to delete"),
):
    """Delete a container application."""
    try:
        api_client.delete(f"/hcs/apps/{app_id}")
        console.print("[green]Successfully deleted application![/green]")
    except APIError as e:
        console.print(f"[red]Error deleting application: {str(e)}[/red]")
        raise typer.Exit(1)
