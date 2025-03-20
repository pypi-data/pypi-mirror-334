"""Environment management commands for HostSpace CLI."""
import typer
from rich.console import Console
from rich.table import Table

from hostspace.utils.config import config

env_app = typer.Typer(help="Manage HostSpace environments")
console = Console()

@env_app.command()
def set(
    environment: str = typer.Argument(
        ...,
        help="Environment to use (production/development)"
    )
):
    """Set the current environment."""
    try:
        config.set_environment(environment)
        console.print(f"[green]Successfully switched to {environment} environment[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@env_app.command()
def show():
    """Show current environment configuration."""
    current_env = config.get_environment()
    endpoint = config.get_endpoint()

    table = Table(title="Environment Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Current Environment", current_env)
    table.add_row("API Endpoint", endpoint)

    console.print(table)
