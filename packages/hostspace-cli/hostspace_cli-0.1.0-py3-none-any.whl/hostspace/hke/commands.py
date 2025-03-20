"""Kubernetes Engine (HKE) commands for HostSpace CLI."""
import typer
from rich.console import Console
from rich.table import Table

from hostspace.utils.api import api_client, APIError

hke_app = typer.Typer(help="Manage Kubernetes Engine (HKE) resources")
console = Console()

@hke_app.command()
def cluster_list():
    """List all Kubernetes clusters."""
    try:
        clusters = api_client.get("/hke/clusters")
        table = Table(title="Kubernetes Clusters")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Region", style="blue")
        table.add_column("Version", style="magenta")

        for cluster in clusters.get("items", []):
            table.add_row(
                str(cluster.get("id")),
                cluster.get("name"),
                cluster.get("status"),
                cluster.get("region"),
                cluster.get("version")
            )
        console.print(table)
    except APIError as e:
        console.print(f"[red]Error listing clusters: {str(e)}[/red]")
        raise typer.Exit(1)

@hke_app.command()
def cluster_create(
    name: str = typer.Option(..., "--name", "-n", help="Cluster name"),
    region: str = typer.Option(..., "--region", "-r", help="Region to deploy in"),
    version: str = typer.Option(..., "--version", "-v", help="Kubernetes version"),
):
    """Create a new Kubernetes cluster."""
    try:
        data = {
            "name": name,
            "region": region,
            "version": version,
        }
        response = api_client.post("/hke/clusters", data)
        console.print("[green]Successfully created cluster![/green]")
        console.print(f"Cluster ID: {response.get('id')}")
    except APIError as e:
        console.print(f"[red]Error creating cluster: {str(e)}[/red]")
        raise typer.Exit(1)

@hke_app.command()
def cluster_delete(
    cluster_id: str = typer.Argument(..., help="ID of the cluster to delete"),
):
    """Delete a Kubernetes cluster."""
    try:
        api_client.delete(f"/hke/clusters/{cluster_id}")
        console.print("[green]Successfully deleted cluster![/green]")
    except APIError as e:
        console.print(f"[red]Error deleting cluster: {str(e)}[/red]")
        raise typer.Exit(1)

@hke_app.command()
def node_pool_add(
    cluster_id: str = typer.Argument(..., help="ID of the cluster"),
    name: str = typer.Option(..., "--name", "-n", help="Node pool name"),
    size: str = typer.Option(..., "--size", "-s", help="Node size"),
    count: int = typer.Option(1, "--count", "-c", help="Number of nodes"),
):
    """Add a node pool to a cluster."""
    try:
        data = {
            "name": name,
            "size": size,
            "count": count,
        }
        response = api_client.post(f"/hke/clusters/{cluster_id}/node-pools", data)
        console.print("[green]Successfully added node pool![/green]")
        console.print(f"Node Pool ID: {response.get('id')}")
    except APIError as e:
        console.print(f"[red]Error adding node pool: {str(e)}[/red]")
        raise typer.Exit(1)
