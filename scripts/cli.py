"""Command-line interface for JARVIS-AI."""

import click
import asyncio
from pathlib import Path


@click.group()
def cli():
    """JARVIS-AI Command Line Interface."""
    pass


@cli.command()
def setup():
    """Setup JARVIS-AI."""
    click.echo("Setting up JARVIS-AI...")
    # TODO: Implement setup
    click.echo("Setup complete!")


@cli.command()
def start():
    """Start JARVIS-AI backend."""
    click.echo("Starting JARVIS-AI backend...")
    # TODO: Implement start
    click.echo("Backend started!")


@cli.command()
def stop():
    """Stop JARVIS-AI backend."""
    click.echo("Stopping JARVIS-AI backend...")
    # TODO: Implement stop
    click.echo("Backend stopped!")


@cli.command()
def test():
    """Run tests."""
    click.echo("Running tests...")
    # TODO: Implement test runner
    click.echo("Tests complete!")


@cli.command()
@click.option('--model', default='mistral', help='Model to pull')
def pull_model(model: str):
    """Pull a model from Ollama."""
    click.echo(f"Pulling {model} from Ollama...")
    # TODO: Implement model pulling
    click.echo(f"{model} pulled successfully!")


if __name__ == "__main__":
    cli()
