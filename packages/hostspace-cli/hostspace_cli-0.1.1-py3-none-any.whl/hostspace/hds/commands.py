"""Database Service (HDS) commands for HostSpace CLI."""
import typer
from rich.console import Console
from rich.table import Table

from hostspace.utils.api import api_client, APIError

hds_app = typer.Typer(help="Manage Database Service (HDS) resources")
console = Console()

@hds_app.command()
def instance_list():
    """List all database instances."""
    try:
        instances = api_client.get("/hds/instances")
        table = Table(title="Database Instances")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Status", style="blue")
        table.add_column("Region", style="magenta")
        table.add_column("Size", style="white")

        for instance in instances.get("items", []):
            table.add_row(
                str(instance.get("id")),
                instance.get("name"),
                instance.get("type"),
                instance.get("status"),
                instance.get("region"),
                instance.get("size")
            )
        console.print(table)
    except APIError as e:
        console.print(f"[red]Error listing instances: {str(e)}[/red]")
        raise typer.Exit(1)

@hds_app.command()
def instance_create(
    name: str = typer.Option(..., "--name", "-n", help="Instance name"),
    type: str = typer.Option(..., "--type", "-t", help="Database type (mysql, postgresql)"),
    region: str = typer.Option(..., "--region", "-r", help="Region to deploy in"),
    size: str = typer.Option(..., "--size", "-s", help="Instance size"),
    version: str = typer.Option(..., "--version", "-v", help="Database version"),
):
    """Create a new database instance."""
    try:
        data = {
            "name": name,
            "type": type,
            "region": region,
            "size": size,
            "version": version,
        }
        response = api_client.post("/hds/instances", data)
        console.print("[green]Successfully created database instance![/green]")
        console.print(f"Instance ID: {response.get('id')}")
    except APIError as e:
        console.print(f"[red]Error creating instance: {str(e)}[/red]")
        raise typer.Exit(1)

@hds_app.command()
def backup_create(
    instance_id: str = typer.Argument(..., help="ID of the database instance"),
    description: str = typer.Option(None, "--description", "-d", help="Backup description"),
):
    """Create a backup of a database instance."""
    try:
        data = {"description": description} if description else {}
        response = api_client.post(f"/hds/instances/{instance_id}/backups", data)
        console.print("[green]Successfully initiated backup![/green]")
        console.print(f"Backup ID: {response.get('id')}")
    except APIError as e:
        console.print(f"[red]Error creating backup: {str(e)}[/red]")
        raise typer.Exit(1)

@hds_app.command()
def backup_list(
    instance_id: str = typer.Argument(..., help="ID of the database instance"),
):
    """List backups for a database instance."""
    try:
        backups = api_client.get(f"/hds/instances/{instance_id}/backups")
        table = Table(title=f"Backups for Instance {instance_id}")
        table.add_column("ID", style="cyan")
        table.add_column("Created At", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Size", style="blue")
        table.add_column("Description", style="white")

        for backup in backups.get("items", []):
            table.add_row(
                str(backup.get("id")),
                backup.get("created_at"),
                backup.get("status"),
                backup.get("size"),
                backup.get("description", "")
            )
        console.print(table)
    except APIError as e:
        console.print(f"[red]Error listing backups: {str(e)}[/red]")
        raise typer.Exit(1)
