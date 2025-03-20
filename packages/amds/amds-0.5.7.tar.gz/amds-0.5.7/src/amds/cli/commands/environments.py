import click
from ..utils import print_json

@click.group()
def environments():
    """Manage environments"""
    pass

@environments.command('list')
@click.pass_obj
def list_environments(client):
    """List all environments"""
    with client as c:
        res = c.environments.get()

        result = res.result
        
        if not result.environments:
            click.echo("No environments found.")
            return

        click.echo("\nAvailable Environments:")
        click.echo("─" * 75)
        
        for env in result.environments:
            click.echo(f"Name:        {click.style(env.name, fg='bright_green')}")
            click.echo(f"ID:          {env.environment_id}")
            if hasattr(env, "description") and env.description:
                click.echo(f"Description: {env.description}")
            click.echo("─" * 75) 

@environments.command('get')
@click.option("--environment-id", required=True, help="ID of the environment")
@click.pass_obj
def get_environment(client, environment_id):
    """Get details of a specific environment by name"""
    with client as c:
        res = c.environments.get()
        result = res.result
        
        if not result.environments:
            click.echo("No environments found.")
            return
            
        environment = next((env for env in result.environments if env.environment_id == environment_id), None)
        
        if environment:
            click.echo("\nEnvironment Details:")
            click.echo("─" * 75)
            click.echo(f"Name:        {click.style(environment.name, fg='bright_green')}")
            click.echo(f"ID:          {environment.environment_id}")
            if hasattr(environment, "description") and environment.description:
                click.echo(f"Description: {environment.description}")
            click.echo("─" * 75)
        else:
            click.echo(f"Environment '{name}' not found", err=True) 