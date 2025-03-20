import click
from minaki.plugin_manager import disable_plugin

@click.command()
@click.argument("plugin_name")
def disable(plugin_name):

    """Disable a Minaki plugin."""
    disable_plugin(plugin_name)
