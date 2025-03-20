import click
import os
import requests
from minaki.plugin_manager import download_plugin

@click.command()
@click.argument("plugin_name")
def install(plugin_name):
    """
    Install a plugin from the Minaki repository.
    """
    download_plugin(plugin_name)
