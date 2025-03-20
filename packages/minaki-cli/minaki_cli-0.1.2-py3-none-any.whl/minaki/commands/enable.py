import click
from minaki.plugin_manager import enable_plugin

@click.command()
@click.argument("plugin_name")
def enable(plugin_name):
    """Enable a Minaki plugin."""
    enable_plugin(plugin_name)
