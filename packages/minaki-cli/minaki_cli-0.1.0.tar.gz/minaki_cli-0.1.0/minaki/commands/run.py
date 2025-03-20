import click
import subprocess

@click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
@click.argument("cmd", nargs=-1, required=True)
def run(cmd):
    """Run any shell command through Minaki"""
    command = " ".join(cmd)
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)
        exit(result.returncode)
    except FileNotFoundError:
        click.echo(f"⚠️ Command not found: {cmd[0]}", err=True)
        exit(127)
    except subprocess.CalledProcessError as e:
        click.echo(f"⚠️ Error executing '{command}': {e}", err=True)
        exit(e.returncode)
