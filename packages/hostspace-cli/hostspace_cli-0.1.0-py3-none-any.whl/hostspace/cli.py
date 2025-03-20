"""Main CLI entry point for HostSpace CLI."""
import typer
from rich.console import Console

from hostspace.auth.commands import auth_app
from hostspace.hke.commands import hke_app
from hostspace.hcs.commands import hcs_app
from hostspace.hds.commands import hds_app
from hostspace.env_commands import env_app

app = typer.Typer(
    name="hs",
    help="HostSpace CLI - Manage your cloud resources",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(auth_app, name="auth")
app.add_typer(hke_app, name="hke")
app.add_typer(hcs_app, name="hcs")
app.add_typer(hds_app, name="hds")
app.add_typer(env_app, name="env")

console = Console()

def main():
    """Main entry point for the CLI."""
    app()
