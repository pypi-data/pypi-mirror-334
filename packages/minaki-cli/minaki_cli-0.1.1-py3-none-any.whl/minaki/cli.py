import click
import os
import importlib.util
from minaki.commands.install import install
from minaki.commands.list_plugins import list  # Avoids conflict
from minaki.commands.update import update
from minaki.commands.enable import enable
from minaki.commands.disable import disable
from minaki.commands.remove import remove
from minaki.commands.run import run  # Shell command wrapper

PLUGIN_DIR = os.path.expanduser("~/.minaki_plugins")

@click.group()
def minaki():
    """Minaki CLI - A modular command execution tool."""
    pass

@click.group()
def plugin():
    """Minaki Plugin Management"""

@click.group()
def app():
    """Run Installed Minaki Applications (Plugins)"""

# Register built-in commands under 'plugin'
plugin.add_command(install)
plugin.add_command(list)
plugin.add_command(update)
plugin.add_command(enable)
plugin.add_command(disable)
plugin.add_command(remove)

# Attach groups to Minaki
minaki.add_command(plugin)
minaki.add_command(run)
minaki.add_command(app)

# Load plugins dynamically into the 'app' group
def load_plugins():
    """Dynamically load installed plugins into 'app'."""
    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR, exist_ok=True)
        return

    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py"):
            plugin_path = os.path.join(PLUGIN_DIR, filename)
            module_name = filename[:-3]  # Remove .py extension

            # Load the plugin dynamically
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Register plugin commands inside 'app'
            if hasattr(module, "plugin") and hasattr(module.plugin, "register_commands"):
                module.plugin.register_commands(app)

# Load plugins dynamically when Minaki starts
load_plugins()

if __name__ == "__main__":
    minaki()
