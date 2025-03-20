import click
import requests

PLUGIN_REPO = "https://api.github.com/repos/minakilabs/minaki-plugins/contents/plugins"

@click.command()
def list():
    """List available plugins from the repository."""
    try:
        response = requests.get(PLUGIN_REPO, timeout=5)
        if response.status_code == 200:
            plugins = [plugin["name"] for plugin in response.json()]
            click.echo("📦 Available Plugins:")
            for plugin in plugins:
                click.echo(f" - {plugin}")
        else:
            click.echo("⚠️ Failed to fetch plugins.")
    except requests.RequestException as e:
        click.echo(f"⚠️ Error fetching plugins: {e}")
