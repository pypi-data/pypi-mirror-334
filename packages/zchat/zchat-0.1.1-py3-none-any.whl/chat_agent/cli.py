"""
Command-line interface for the chat agent.
"""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .config import config
from .main import ChatAgent
from .storage import ChatSession

app = typer.Typer(help="A personal chat agent using Together AI via AirTrain.")
console = Console()

# Define command names to prioritize over session IDs
COMMAND_NAMES = ["list", "info", "chat"]


def find_session_by_partial_id(partial_id: str) -> Optional[str]:
    """Find a session by partial ID match (prefix)."""
    if not partial_id:
        return None

    sessions = ChatSession.list_sessions()
    for session in sessions:
        if session["session_id"].startswith(partial_id):
            return session["session_id"]
    return None


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    session_id: Optional[str] = typer.Argument(
        None, help="Session ID to continue (can be partial)"
    ),
):
    """Run the chat command if no command is provided."""
    # Check if a subcommand is being used
    if ctx.invoked_subcommand is not None:
        # A subcommand is being used, don't process session_id
        return

    # Check if session_id matches a command name
    if session_id in COMMAND_NAMES:
        # This is likely a command being mistaken for a session ID
        console.print(f"[red]'{session_id}' is a command, not a session ID.[/red]")
        console.print(f"To use the {session_id} command, try: z {session_id}")
        return

    # If a session ID is provided as an argument, try to continue that session
    if session_id:
        # Try to find a session with a matching prefix
        full_session_id = find_session_by_partial_id(session_id)
        if full_session_id:
            console.print(f"Continuing session: [cyan]{full_session_id}[/cyan]")
            # Don't call the chat function directly to avoid Typer's parameter handling issue
            _start_chat(session_id=full_session_id)
        else:
            console.print(f"[red]No session found starting with '{session_id}'[/red]")
            console.print("Use 'z list' to see available sessions.")
    else:
        # Start a new chat session if no session ID provided
        _start_chat(session_id=None)


def _start_chat(session_id: Optional[str] = None):
    """Start a chat session without Typer's parameter handling."""
    agent = ChatAgent(session_id=session_id)
    agent.chat()


@app.command()
def chat(
    session_id: Optional[str] = typer.Option(
        None,
        "--continue",
        "-c",
        help="Continue an existing chat session (can be partial ID).",
    )
):
    """Start a chat session with the AI."""
    # If session_id is provided, try to find a match with a partial ID
    if session_id:
        full_id = find_session_by_partial_id(session_id)
        if full_id:
            session_id = full_id
            console.print(f"Continuing session: [cyan]{full_id}[/cyan]")
        else:
            console.print(f"[red]No session found starting with '{session_id}'[/red]")
            console.print("Use 'z list' to see available sessions.")
            return

    _start_chat(session_id=session_id)


@app.command("list")
def list_sessions():
    """List all available chat sessions."""
    sessions = ChatSession.list_sessions()

    if not sessions:
        console.print("[yellow]No chat sessions found.[/yellow]")
        return

    table = Table(title="Available Chat Sessions")
    table.add_column("Session ID", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("Messages", style="blue")
    table.add_column("Preview", style="yellow")

    for session in sessions:
        table.add_row(
            session["session_id"],
            session["created_at"],
            str(session["message_count"]),
            session.get("preview", "No preview available"),
        )

    console.print(table)


@app.command("info")
def storage_info():
    """Show information about the chat storage location."""
    console.print("Chat history storage location:")
    console.print(f"[green]{config.storage_dir}[/green]")

    # Check if the directory exists
    if config.storage_dir.exists():
        console.print("Directory exists: [green]Yes[/green]")
        sessions = ChatSession.list_sessions()
        console.print(f"Number of sessions: [blue]{len(sessions)}[/blue]")
    else:
        console.print("Directory exists: [red]No[/red]")
        console.print(
            "[yellow]The directory will be created when you start a chat.[/yellow]"
        )


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
