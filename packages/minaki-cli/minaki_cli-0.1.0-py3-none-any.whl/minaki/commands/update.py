import click
from minaki.plugin_manager import download_plugin

@click.command()
@click.argument("plugin_name")
def update(plugin_name):
    """Update an installed plugin."""
    download_plugin(plugin_name)
