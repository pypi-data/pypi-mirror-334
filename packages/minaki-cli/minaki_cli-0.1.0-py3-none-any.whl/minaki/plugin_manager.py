import os
import requests
import click
import json

#PLUGIN_REPO = "https://raw.githubusercontent.com/minakilabs/minaki-plugins/main/plugins/"
PLUGIN_REPO = "https://raw.githubusercontent.com/minakilabs/minaki-plugins/master/"

PLUGIN_DIR = os.path.expanduser("~/.minaki_plugins")
CONFIG_FILE = os.path.join(PLUGIN_DIR, "enabled_plugins.json")

# Ensure the plugin directory exists
os.makedirs(PLUGIN_DIR, exist_ok=True)

# Ensure the config file exists
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump([], f)


def download_plugin(plugin_name):
    """Download a plugin from the Minaki GitHub repository."""
    url = f"{PLUGIN_REPO}{plugin_name}.py"
    plugin_path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(plugin_path, "w") as f:
                f.write(response.text)
            click.echo(f"✅ Plugin '{plugin_name}' installed successfully at {plugin_path}.")
        else:
            click.echo(f"⚠️ Plugin '{plugin_name}' not found in repo.")
    except requests.RequestException as e:
        click.echo(f"⚠️ Error downloading plugin: {e}")


def list_plugins():
    """List available plugins from the GitHub repository."""
    try:
        response = requests.get(PLUGIN_REPO, timeout=5)
        if response.status_code == 200:
            plugins = [item['name'].replace('.py', '') for item in response.json() if item['name'].endswith(".py")]
            click.echo("📦 Available Plugins:")
            for plugin in plugins:
                click.echo(f" - {plugin}")
            return plugins
        else:
            click.echo("⚠️ Could not fetch plugin list.")
            return []
    except requests.RequestException as e:
        click.echo(f"⚠️ Error fetching plugin list: {e}")
        return []


def enable_plugin(plugin_name):
    """Enable a plugin by adding it to the active plugins list."""
    plugin_path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")

    if not os.path.exists(plugin_path):
        click.echo(f"⚠️ Plugin '{plugin_name}' not found. Install it first.")
        return

    with open(CONFIG_FILE, "r+") as f:
        enabled_plugins = json.load(f)
        if plugin_name in enabled_plugins:
            click.echo(f"⚠️ Plugin '{plugin_name}' is already enabled.")
            return
        enabled_plugins.append(plugin_name)
        f.seek(0)
        json.dump(enabled_plugins, f)
        f.truncate()

    click.echo(f"✅ Plugin '{plugin_name}' enabled.")


def disable_plugin(plugin_name):
    """Disable a plugin by removing it from the active plugins list."""
    with open(CONFIG_FILE, "r+") as f:
        enabled_plugins = json.load(f)
        if plugin_name not in enabled_plugins:
            click.echo(f"⚠️ Plugin '{plugin_name}' is not enabled.")
            return
        enabled_plugins.remove(plugin_name)
        f.seek(0)
        json.dump(enabled_plugins, f)
        f.truncate()

    click.echo(f"✅ Plugin '{plugin_name}' disabled.")


def list_enabled_plugins():
    """List currently enabled plugins."""
    with open(CONFIG_FILE, "r") as f:
        enabled_plugins = json.load(f)

    if enabled_plugins:
        click.echo("✅ Enabled Plugins:")
        for plugin in enabled_plugins:
            click.echo(f" - {plugin}")
    else:
        click.echo("⚠️ No plugins enabled.")
