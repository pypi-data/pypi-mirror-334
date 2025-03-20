import click
import os

@click.command()
@click.argument("plugin_name")
def remove(plugin_name):
    """Remove an installed plugin."""
    plugin_path = os.path.expanduser(f"~/.minaki_plugins/{plugin_name}.py")
    if os.path.exists(plugin_path):
        os.remove(plugin_path)
        click.echo(f"✅ Plugin '{plugin_name}' removed successfully.")
    else:
        click.echo(f"⚠️ Plugin '{plugin_name}' not found.")
