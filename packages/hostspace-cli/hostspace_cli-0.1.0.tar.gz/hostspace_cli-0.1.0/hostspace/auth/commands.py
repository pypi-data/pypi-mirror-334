"""Authentication commands for HostSpace CLI."""
import typer
from rich.console import Console
from rich.table import Table

from hostspace.utils.config import config
from hostspace.utils.api import api_client, APIError

auth_app = typer.Typer(help="Manage authentication and API keys")
console = Console()

@auth_app.command()
def login(api_key: str = typer.Option(
    None,
    "--api-key",
    "-k",
    help="API key for authentication",
    prompt="Please enter your API key",
    hide_input=True
)):
    """Log in to HostSpace using your API key."""
    try:
        config.set_api_key(api_key)
        # Test the API key
        api_client._setup_session()
        api_client.get("/auth/verify")
        console.print("[green]Successfully logged in to HostSpace![/green]")
    except APIError as e:
        config.set_api_key(None)
        console.print(f"[red]Login failed: {str(e)}[/red]")
        raise typer.Exit(1)

@auth_app.command()
def logout():
    """Log out and remove stored credentials."""
    config.set_api_key(None)
    console.print("[yellow]Logged out successfully[/yellow]")

@auth_app.command()
def status():
    """Show current authentication status."""
    api_key = config.get_api_key()
    endpoint = config.get_endpoint()

    table = Table(title="Authentication Status")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("API Endpoint", endpoint)
    table.add_row(
        "API Key",
        "Configured" if api_key else "Not configured",
    )

    console.print(table)
