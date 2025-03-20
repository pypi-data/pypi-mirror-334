import click
from ..utils import print_json
import webbrowser


@click.group()
def servers():
    """Manage servers"""
    pass


@servers.command("list")
@click.pass_obj
def list_servers(client):
    """List all servers"""
    with client as c:
        res = c.servers.get()
        servers = res.result.servers
        # Print header
        click.echo(
            f"{'NAME':<20} {'ENVIRONMENT':<15} {'TYPE':<20} {'STATUS':<10} {'PORT'}"
        )
        click.echo("-" * 75)
        # Print each server's info
        for server in servers:
            click.echo(
                f"{server.name:<20} "
                f"{server.environment:<15} "
                f"{server.server_request:<20} "
                f"{server.status:<10} "
                f"{int(server.port)}"
            )


@servers.command("get")
@click.option("--server-name", required=True, help="Name of the server")
@click.pass_obj
def get_server(client, server_name):
    """Get server information"""
    with client as c:
        res = c.servers.get()
        servers = res.result.servers
        server = next((s for s in servers if s.name == server_name), None)
        if server:
            click.echo("\nServer Details:")
            click.echo("─" * 75)
            click.echo(f"Name:        {server.name}")
            click.echo(f"Environment: {server.environment}")
            click.echo(f"Type:        {server.server_request}")
            click.echo(f"Status:      {server.status}")
            click.echo(f"Port:        {int(server.port)}")
            if server.alph_editor_url:
                click.echo(
                    f"Alph Editor URL: {click.style(server.alph_editor_url, fg='bright_blue', underline=True)}"
                )
            if server.url:
                click.echo(
                    f"Jupyter Lab URL: {click.style(server.url, fg='bright_blue', underline=True)}"
                )
            if server.port_forward_url:
                click.echo(
                    f"Port Forward URL: {click.style(server.port_forward_url, fg='bright_blue', underline=True)}"
                )
            click.echo("─" * 75)
        else:
            click.echo(f"Server '{server_name}' not found", err=True)


@servers.command("create")
@click.option("--name", required=True, help="Name of the server")
@click.option("--environment", default="ai", help="Server environment")
@click.option("--port", type=int, default=5000, help="Server port")
@click.option("--server-type", default="amds-medium_cpu", help="Server type/request")
@click.pass_obj
def create_server(client, name, environment, port, server_type):
    """Create a server"""
    with client as c:
        res = c.servers.create(
            request={
                "environment": environment,
                "port": port,
                "server_name": name,
                "server_request": server_type,
            }
        )
        result = res.result

        click.echo(click.style("\nServer Created Successfully!", fg="green"))
        click.echo("─" * 75)
        click.echo(f"Name:        {result.server_name}")
        click.echo(f"Environment: {result.environment}")
        click.echo(f"Type:        {result.server_request}")
        click.echo(f"Port:        {int(result.port)}")
        click.echo(f"Status:      {result.status}")
        if result.hourly_rate:
            click.echo(f"Hourly Rate: ${result.hourly_rate/100:.2f}")

        if result.alph_editor_url:
            click.echo(
                f"\nAlph Editor URL: {click.style(result.alph_editor_url, fg='bright_blue', underline=True)}"
            )
        if result.url:
            click.echo(
                f"Jupyter Lab URL:\033]8;;{result.url}\033\\{result.url}\033]8;;\033\\"
            )
        if result.port_forward_url:
            click.echo(
                f"Forward URL: \033]8;;{result.port_forward_url}\033\\{result.port_forward_url}\033]8;;\033\\"
            )
        click.echo("─" * 75)


@servers.command("stop")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.option("--environment", required=False, default="ai", help="Server environment")
@click.option("--port", type=int, required=False, default=5000, help="Server port")
@click.option(
    "--server-type", required=False, default="amds-medium_cpu", help="Server type"
)
@click.pass_obj
def stop_server(client, server_name, force, environment, port, server_type):
    """Stop a server"""
    if not force and not click.confirm(f"Are you sure you want to stop server '{server_name}'?"):
        click.echo("Operation cancelled.")
        return
        
    with client as c:
        res = c.servers.stop(server_name=server_name)
        click.echo(click.style(f"\nServer '{server_name}' stopped successfully ✔", fg="green"))


@servers.command("start")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--environment", required=False, default="ai", help="Server environment")
@click.option("--port", type=int, required=False, default=5000, help="Server port")
@click.option(
    "--server-type", required=False, default="amds-medium_cpu", help="Server type"
)
@click.pass_obj
def start_server(client, server_name, environment, port, server_type):
    """Start a server"""
    with client as c:
        res = c.servers.start(
            server_name=server_name,
            environment=environment,
            port=port,
            server_request=server_type,
        )
        result = res.result

        click.echo(click.style("\nServer Started Successfully!", fg="green"))
        click.echo("─" * 75)
        click.echo(f"Name:        {result.server_name}")
        click.echo(f"Environment: {result.environment}")
        click.echo(f"Type:        {result.server_request}")
        click.echo(f"Port:        {int(result.port)}")
        click.echo(f"Status:      {result.status}")
        if result.hourly_rate:
            click.echo(f"Hourly Rate: ${result.hourly_rate/100:.2f}")

        if result.alph_editor_url:
            click.echo(f"\nAlph Editor URL: {result.alph_editor_url}")
        if result.url:
            click.echo(
                f"Jupyter Lab URL: \033]8;;{result.url}\033\\{result.url}\033]8;;\033\\"
            )
        if result.port_forward_url:
            click.echo(
                f"Port Forward URL: \033]8;;{result.port_forward_url}\033\\{result.port_forward_url}\033]8;;\033\\"
            )
        click.echo("─" * 75)


@servers.command("delete")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.pass_obj
def delete_server(client, server_name, force):
    """Delete a server"""
    if not force and not click.confirm(f"Are you sure you want to delete server '{server_name}'?"):
        click.echo("Operation cancelled.")
        return
        
    with client as c:
        res = c.servers.delete(server_name=server_name)
        click.echo(
            click.style(f"\nServer '{server_name}' deleted successfully ✔", fg="green")
        )


@servers.command("get-file", hidden=True)
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--path", required=True, help="Remote file path")
@click.pass_obj
def get_file(client, server_name, path):
    """Get a file from a server"""
    with client as c:
        res = c.servers.get_file(server_name=server_name, path=path)
        print_json(res.model_dump())


@servers.command("upload-file", hidden=True)
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--path", required=True, help="Remote file path")
@click.option("--content", help="File content")
@click.option("--format", "format_", default="text", help="File format")
@click.option("--type", "type_", default="file", help="Content type")
@click.pass_obj
def upload_file(client, server_name, path, content, format_, type_):
    """Upload a file to a server"""
    with client as c:
        res = c.servers.upload_file(
            server_name=server_name,
            path=path,
            content=content,
            format_=format_,
            type_=type_,
        )
        print_json(res.model_dump())


@servers.command("run-code", hidden=True)
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--code", help="Python code to execute")
@click.option("--kernel-name", default="api-kernel", help="Kernel name")
@click.pass_obj
def run_code(client, server_name, code, kernel_name):
    """Run code on a server"""
    with client as c:
        res = c.servers.run_code(
            server_name=server_name, code=code, kernel_name=kernel_name
        )
        print_json(res.model_dump())


@servers.command("open")
@click.option("--server-name", required=True, help="Name of the server")
@click.pass_obj
def open_server_editor(client, server_name):
    """Open Alph Editor for a server in the default browser"""
    with client as c:
        res = c.servers.get()
        servers = res.result.servers
        server = next((s for s in servers if s.name == server_name), None)
        
        if server:
            # Check server status before proceeding
            if server.status.lower() not in ["running", "ready"]:
                click.echo(f"Server '{server_name}' is not running (status: {server.status})", err=True)
                click.echo("Please start the server before opening the editor.")
                return
                
            if server.alph_editor_url:
                click.echo(f"Opening Alph Editor for '{server_name}'...")
                webbrowser.open(server.alph_editor_url)
            else:
                click.echo(f"No Alph Editor URL available for server '{server_name}'", err=True)
        else:
            click.echo(f"Server '{server_name}' not found", err=True)
