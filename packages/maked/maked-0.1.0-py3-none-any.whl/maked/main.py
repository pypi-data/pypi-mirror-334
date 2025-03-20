import sys

import yaml
import subprocess
import click

@click.command()
@click.argument("filename", type=click.Path(exists=True), required=False)
def cli(filename):
    """Reads a Markdown file, extracts the command from the YAML front matter, and executes it."""
    if filename:
        with open(filename, 'r') as file:
            content = file.readlines()
    else:
        # If no input_file is provided, read from stdin
        content = sys.stdin.readlines()
    
    # Check if content is empty before processing further
    if not content:
        click.echo("No content received.")
        return

    # Look for YAML front matter
    if content[0].strip() == "---":
        try:
            end_idx = content[1:].index("---\n") + 1
            metadata = yaml.safe_load("".join(content[1:end_idx]))
            if "maked" in metadata:
                command = metadata["maked"]
                click.echo(f"Executing command: {command}")
                subprocess.run(command, shell=True)
            else:
                click.echo("No 'maked' field found in the YAML front matter.")
        except (ValueError, yaml.YAMLError):
            click.echo("Error parsing YAML front matter.")
    else:
        click.echo("No YAML front matter found.")

if __name__ == "__main__":
    cli()

