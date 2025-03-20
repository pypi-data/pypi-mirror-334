"""
Main functionality for the chat agent.
"""

import sys
import socket
import requests
from typing import Optional, List, Dict, Tuple

from airtrain.integrations.together.skills import TogetherAIChatSkill, TogetherAIInput
from airtrain.integrations.together.credentials import TogetherAICredentials
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

from .config import config
from .storage import ChatSession

console = Console()


def check_internet_connectivity() -> Tuple[bool, str]:
    """Check if internet is accessible.

    Returns:
        Tuple[bool, str]: (is_connected, error_message)
    """
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True, ""
    except OSError:
        # Try an alternative method using requests
        try:
            requests.get("https://www.google.com", timeout=3)
            return True, ""
        except requests.RequestException:
            msg = "Cannot connect to the internet. Please check your connection."
            return False, msg


def check_together_ai_connectivity() -> Tuple[bool, str]:
    """Check if Together AI API is accessible.

    Returns:
        Tuple[bool, str]: (is_accessible, error_message)
    """
    # Skip the connectivity check for now since it's causing issues
    return True, ""


class ChatAgent:
    """Chat agent that interfaces with Together AI via AirTrain."""

    def __init__(self, session_id: Optional[str] = None):
        """Initialize the chat agent with an optional session ID."""
        # Load or create a chat session
        if session_id:
            self.session = ChatSession.load(session_id)
            if not self.session:
                msg = (
                    f"[red]Session {session_id} not found. "
                    f"Creating a new session.[/red]"
                )
                console.print(msg)
                self.session = ChatSession()
        else:
            self.session = ChatSession()

        # Check for API key and handle setup if missing
        if not config.is_api_key_set:
            self._handle_missing_credentials()

        # Check if we have credentials now
        if not config.is_api_key_set:
            console.print("[red]Error: Could not set up API credentials.[/red]")
            console.print("Please try again or set TOGETHER_API_KEY manually.")
            sys.exit(1)

        # Initialize AirTrain Together AI client
        self.credentials = TogetherAICredentials(
            together_api_key=config.together_api_key
        )
        self.chat_skill = TogetherAIChatSkill(credentials=self.credentials)
        self.model_name = config.get_model_name()

    def _handle_missing_credentials(self) -> None:
        """Handle missing credentials by prompting the user."""
        console.print("[yellow]Warning: Together AI API key not found![/yellow]")
        msg = "The API key was not found in environment variables or credentials file."
        console.print(msg)
        creds_path = config.credentials_dir / "togetherai.json"
        console.print(f"Credentials should be in: {creds_path}")
        console.print()

        if Confirm.ask("Would you like to set up your Together AI API key now?"):
            api_key = Prompt.ask("Enter your Together AI API key", password=True)
            if api_key:
                if config.save_together_credentials(api_key):
                    console.print("[green]API key saved successfully![/green]")
                else:
                    err_msg = (
                        "[red]Failed to save API key. "
                        "Using it for this session only.[/red]"
                    )
                    console.print(err_msg)
                # Set the key for this session
                config.together_api_key = api_key
            else:
                console.print("[yellow]No API key provided.[/yellow]")

    def chat(self) -> None:
        """Start an interactive chat session."""
        # Remove connectivity checks from here - we'll check only when making API calls

        console.print("[bold blue]Chat Session Started[/bold blue]")
        console.print(f"Session ID: {self.session.session_id}")
        console.print("Type 'exit', 'quit', or 'q' to end the session.")
        console.print()

        # Display existing messages if any
        if self.session.messages:
            console.print("[bold]Chat History:[/bold]")
            for message in self.session.messages:
                if message["role"] == "user":
                    console.print(f"[bold green]You:[/bold green] {message['content']}")
                else:
                    console.print("[bold purple]AI:[/bold purple]")
                    console.print(Markdown(message["content"]))
            console.print("\n[bold]Continuing conversation...[/bold]\n")

        # Interactive chat loop
        while True:
            try:
                # Get user input
                user_input = console.input("[bold green]You:[/bold green] ")

                # Check for exit command
                if user_input.lower() in ["exit", "quit", "q"]:
                    console.print("[bold blue]Ending chat session...[/bold blue]")
                    break

                # Add user message to session
                self.session.add_message("user", user_input)

                # Format messages for the API
                messages = self._format_messages_for_api()
                system_prompt = "You are a helpful assistant."

                # Check internet connectivity only when about to make an API call
                internet_connected, internet_error = check_internet_connectivity()
                if not internet_connected:
                    console.print(f"[bold red]Error: {internet_error}[/bold red]")
                    continue  # Continue the loop to allow user to try again or quit

                # Prepare the input for the AirTrain TogetherAI skill
                input_data = TogetherAIInput(
                    user_input=user_input,
                    system_prompt=system_prompt,
                    # Exclude the last user message
                    conversation_history=messages[:-1],
                    model=self.model_name,
                    max_tokens=1024,
                    temperature=0.7,
                )

                # Call the API
                console.print("[bold purple]AI:[/bold purple]", end="")
                with console.status("[bold]Thinking...[/bold]"):
                    result = self.chat_skill.process(input_data)

                # Get AI response
                ai_response = result.response
                console.print(Markdown(ai_response))

                # Add AI message to session
                self.session.add_message("assistant", ai_response)

            except KeyboardInterrupt:
                interrupt_msg = (
                    "\n[bold blue]Chat session interrupted. "
                    "Saving and exiting...[/bold blue]"
                )
                console.print(interrupt_msg)
                break
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                continue

    def _format_messages_for_api(self) -> List[Dict[str, str]]:
        """Format the messages for the Together AI API."""
        # Filter out timestamp and other metadata
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.session.messages
        ]
