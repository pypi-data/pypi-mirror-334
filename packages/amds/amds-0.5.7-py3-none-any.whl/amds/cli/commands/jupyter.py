import click
import os
import sys
import json
import subprocess
import shutil
import tempfile
import webbrowser
import requests
import time
from pathlib import Path
from ..utils import print_json
import socket
import random
import string
from urllib.parse import urlparse
import threading
import signal
import hashlib
import re
import queue


def create_jupyter_config(
    config_dir,
    allow_origin="https://*.amdatascience.com",
    disable_sudo=False,
):
    """
    Create a Jupyter config file with CORS settings
    """
    # Create the config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Create a jupyter_server_config.py file with CORS configuration
    config_file = os.path.join(config_dir, "jupyter_server_config.py")

    sudo_config = ""
    if disable_sudo:
        sudo_config = """
# Disable sudo/root access
c.ServerApp.allow_root = False
c.ServerApp.allow_sudo = False
"""

    with open(config_file, "w") as f:
        f.write(
            f"""
# Configuration file for jupyter-server.

c = get_config()

# Configure CORS settings
c.ServerApp.allow_origin = '{allow_origin}'
c.ServerApp.allow_credentials = True
c.ServerApp.allow_methods = ['*']
c.ServerApp.allow_headers = ['Content-Type', 'Authorization', 'X-Requested-With', 
                            'X-XSRFToken', 'ngrok-skip-browser-warning', 'Origin', 
                            'Accept', 'Cache-Control', 'X-Requested-With', '*']
{sudo_config}
"""
        )

    return config_file


@click.group()
def jupyter():
    """Connect with local Jupyter Lab"""
    pass


@jupyter.command("launch")
@click.option("--port", type=int, default=8888, help="Port to run Jupyter Lab on")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically")
@click.option(
    "--directory", type=str, default=".", help="Directory to launch Jupyter Lab in"
)
@click.option(
    "--tunnel-provider",
    type=click.Choice(["ngrok", "cloudflare"]),
    default="cloudflare",
    help="Tunnel provider to use (ngrok or cloudflare)",
)
@click.option(
    "--ngrok-port",
    type=int,
    default=None,
    help="Port for ngrok to use (defaults to same as Jupyter port)",
)
@click.option(
    "--app-port",
    type=int,
    default=None,
    help="Additional port to tunnel for your application (stored as port_forward_url)",
)
@click.option(
    "--ngrok-domain",
    type=str,
    default=None,
    help="Domain for ngrok to use (required for Pay-as-you-go plans)",
)
@click.option(
    "--ngrok-region",
    type=click.Choice(["us", "eu", "ap", "au", "sa", "jp", "in"]),
    default="us",
    help="Region for ngrok tunnel",
)
@click.option(
    "--api-key", envvar="AMDS_API_KEY", help="API key for dashboard integration"
)
@click.option("--allow-origin", type=str, default="*", help="CORS allow-origin setting")
@click.option(
    "--disable-sudo", is_flag=True, help="Disable sudo/root permissions in the notebook"
)
@click.option(
    "--output-format",
    type=click.Choice(["standard", "minimal", "json"]),
    default="standard",
    help="Output format for command results",
)
@click.option(
    "--thumbnail",
    type=str,
    default=None,
    help="Custom thumbnail URL for dashboard display",
)
@click.pass_obj
def launch_jupyter(
    client,
    port,
    no_browser,
    directory,
    tunnel_provider,
    ngrok_port,
    app_port,
    ngrok_domain,
    ngrok_region,
    api_key,
    allow_origin,
    disable_sudo,
    output_format,
    thumbnail,
):
    """Launch a Jupyter Lab server locally with ngrok/cloudflare proxy and upload to dashboard.amdatascience.com"""

    # Check if jupyter is installed
    import shutil

    if not shutil.which("jupyter"):
        click.secho(
            "Error: Jupyter Lab is not installed. Please install it with:", fg="red"
        )
        click.echo("    pip install jupyterlab")
        sys.exit(1)

    # Check if tunnel provider is installed
    if tunnel_provider == "ngrok" and not shutil.which("ngrok"):
        click.secho(
            "Error: ngrok is not installed. Please install it from https://ngrok.com/download",
            fg="red",
        )
        sys.exit(1)
    elif tunnel_provider == "cloudflare" and not shutil.which("cloudflared"):
        click.secho(
            "Error: cloudflared is not installed. Please install it from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/",
            fg="red",
        )
        sys.exit(1)

    # Check if port is in use and find an alternative if needed
    if is_port_in_use(port):
        click.secho(f"Warning: Port {port} is already in use.", fg="yellow")
        new_port = find_free_port(port + 1)
        if new_port:
            click.secho(f"Using alternative port {new_port} instead.", fg="yellow")
            port = new_port
        else:
            click.secho(
                "Error: Could not find an available port. Please specify a different port with --port.",
                fg="red",
            )
            sys.exit(1)

    # If ngrok_port is specified, check if it's in use
    if ngrok_port and is_port_in_use(ngrok_port):
        click.secho(f"Warning: ngrok port {ngrok_port} is already in use.", fg="yellow")
        new_ngrok_port = find_free_port(ngrok_port + 1)
        if new_ngrok_port:
            click.secho(
                f"Using alternative ngrok port {new_ngrok_port} instead.", fg="yellow"
            )
            ngrok_port = new_ngrok_port
        else:
            click.secho(
                "Error: Could not find an available ngrok port. Please specify a different port with --ngrok-port.",
                fg="red",
            )
            sys.exit(1)

    # If app_port is specified, check if it's in use
    app_tunnel_url = None
    if app_port:
        if is_port_in_use(app_port):
            click.secho(f"Warning: App port {app_port} is already in use.", fg="yellow")
            new_app_port = find_free_port(app_port + 1)
            if new_app_port:
                click.secho(f"Using alternative app port {new_app_port} instead.", fg="yellow")
                app_port = new_app_port
            else:
                click.secho(
                    "Error: Could not find an available app port. Please specify a different port with --app-port.",
                    fg="red",
                )
                sys.exit(1)

    # If ngrok_port is not specified, use the same as Jupyter port
    if not ngrok_port:
        ngrok_port = port

    # Create a temporary directory for Jupyter config
    jupyter_dir = tempfile.mkdtemp(prefix="jupyter-amds-")

    try:
        # Create Jupyter config with CORS settings
        config_file = create_jupyter_config(jupyter_dir, allow_origin, disable_sudo)
        click.secho(
            f"Created Jupyter config with CORS allow-origin: {allow_origin}", fg="blue"
        )
        if disable_sudo:
            click.echo(
                "Root/sudo permissions have been disabled in the notebook server"
            )

        # Start Jupyter Lab process
        click.echo(f"Starting Jupyter Lab on port {port}...")
        jupyter_cmd = [
            "jupyter",
            "lab",
            f"--port={port}",
            "--no-browser",
            f"--notebook-dir={directory}",
            "--ip=0.0.0.0",
            f"--config={config_file}",
        ]

        # Start Jupyter process
        jupyter_process = subprocess.Popen(
            jupyter_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # Wait for Jupyter to start and get the token
        token = None
        jupyter_url = None
        for line in iter(jupyter_process.stderr.readline, ""):
            if "http://localhost:" in line or "http://127.0.0.1:" in line:
                # Extract just the URL part, removing the log prefix
                url_part = re.search(r"(http://[^\s]+)", line)
                if url_part:
                    jupyter_url = url_part.group(0).strip()
                    token = jupyter_url.split("token=")[-1].strip()
                    break
                else:
                    # Fallback to old method if regex fails
                    jupyter_url = line.strip().split("or ")[-1].strip()
                    token = jupyter_url.split("token=")[-1].strip()
                    break

            sys.stderr.write(line)

            if not token and "ERROR" in line:
                click.secho(
                    "Error starting Jupyter Lab. Please check the logs above.",
                    fg="red",
                    bold=True,
                )
                jupyter_process.terminate()
                sys.exit(1)

        if not token:
            click.secho(
                "Error: Could not get Jupyter token. Exiting.", fg="red", bold=True
            )
            jupyter_process.terminate()
            sys.exit(1)

        click.secho("✓ Jupyter Lab started successfully", fg="green", bold=True)

        # Short delay to ensure all output is captured
        time.sleep(0.5)

        # Start tunnel based on selected provider
        if tunnel_provider == "ngrok":
            # Existing ngrok tunnel code
            click.secho(
                f"Starting ngrok tunnel to port {port}...", fg="blue", bold=True
            )
            ngrok_cmd = [
                "ngrok",
                "http",
                f"{port}",
                "--log=stdout",
            ]

            # Only add region if specified (since it's deprecated according to the error message)
            if ngrok_region:
                ngrok_cmd.append(f"--region={ngrok_region}")

            if ngrok_domain:
                ngrok_cmd.append(f"--domain={ngrok_domain}")
            else:
                click.secho(
                    "Note: If you're using a Pay-as-you-go ngrok plan, you must specify a registered domain with --ngrok-domain",
                    fg="yellow",
                )

            tunnel_process = subprocess.Popen(
                ngrok_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            # Wait for ngrok to start and get the public URL
            tunnel_url = None
            pay_as_you_go_error = False
            for line in iter(tunnel_process.stdout.readline, ""):
                if "url=" in line:
                    tunnel_url = line.split("url=")[1].strip()
                    break

                sys.stdout.write(line)

                # Check for Pay-as-you-go specific error
                if "Your account is on the 'Pay-as-you-go' plan" in line:
                    pay_as_you_go_error = True

                if "error" in line.lower():
                    if pay_as_you_go_error:
                        click.secho(
                            "\nError: Your ngrok account is on the Pay-as-you-go plan, which requires a registered domain.",
                            fg="red",
                            bold=True,
                        )
                        click.echo("Please follow these steps:")
                        click.echo(
                            "1. Register a domain at https://dashboard.ngrok.com/domains"
                        )
                        click.echo(
                            "2. Restart this command with the --ngrok-domain option:"
                        )
                        click.echo(
                            f"   amds jupyter launch --ngrok-domain=your-domain.ngrok.io [other options]"
                        )
                    else:
                        click.echo(
                            "Error starting ngrok tunnel. Please check the logs above."
                        )

                    jupyter_process.terminate()
                    tunnel_process.terminate()
                    sys.exit(1)

            if not tunnel_url:
                click.secho(
                    "Error: Could not get ngrok URL. Exiting.", fg="red", bold=True
                )
                jupyter_process.terminate()
                tunnel_process.terminate()
                sys.exit(1)

            click.secho(f"ngrok tunnel created at {tunnel_url}", fg="green")
            
            # Start additional tunnel for app port if specified
            if app_port:
                click.secho(
                    f"Starting additional ngrok tunnel for application port {app_port}...", fg="blue", bold=True
                )
                app_ngrok_cmd = [
                    "ngrok",
                    "http",
                    f"{app_port}",
                    "--log=stdout",
                ]
                
                # Add region and domain options if specified
                if ngrok_region:
                    app_ngrok_cmd.append(f"--region={ngrok_region}")
                if ngrok_domain:
                    # Generate a subdomain for the app port
                    app_domain = ngrok_domain.replace(".", f"-app.")
                    app_ngrok_cmd.append(f"--domain={app_domain}")
                
                # Start the additional tunnel in a separate process
                app_tunnel_process = subprocess.Popen(
                    app_ngrok_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                )
                
                # Wait for app tunnel to start and get the public URL
                for line in iter(app_tunnel_process.stdout.readline, ""):
                    if "url=" in line:
                        app_tunnel_url = line.split("url=")[1].strip()
                        break
                    
                    sys.stdout.write(line)
                    
                    if "error" in line.lower():
                        click.echo(
                            "Warning: Error starting additional ngrok tunnel for app port. Continuing without app tunnel."
                        )
                        break
                
                if app_tunnel_url:
                    click.secho(f"Additional ngrok tunnel for app port created at {app_tunnel_url}", fg="green")
                else:
                    click.secho(
                        "Warning: Could not create additional tunnel for app port. Continuing without app tunnel.",
                        fg="yellow",
                    )

        elif tunnel_provider == "cloudflare":
            # Cloudflare tunnel implementation
            click.secho(
                f"Starting Cloudflare tunnel to port {port}...", fg="blue", bold=True
            )
            cloudflare_cmd = [
                "cloudflared",
                "tunnel",
                "--url",
                f"http://localhost:{port}",
            ]

            tunnel_process = subprocess.Popen(
                cloudflare_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            # Wait for cloudflare tunnel to start and get the public URL
            tunnel_url = None

            # Create a queue for the output lines
            output_queue = queue.Queue()

            # Define reader functions for stdout and stderr
            def reader(stream, queue):
                for line in iter(stream.readline, ""):
                    queue.put(line)
                stream.close()

            # Start reader threads for both stdout and stderr
            threading.Thread(
                target=reader, args=(tunnel_process.stdout, output_queue), daemon=True
            ).start()
            threading.Thread(
                target=reader, args=(tunnel_process.stderr, output_queue), daemon=True
            ).start()

            # Process the output lines
            timeout = time.time() + 60  # 60 seconds timeout
            while time.time() < timeout:
                try:
                    # Get line with timeout to avoid blocking forever
                    line = output_queue.get(timeout=1)
                    sys.stdout.write(line)

                    # Look for the cloudflare tunnel URL in both streams
                    if "https://" in line and "trycloudflare.com" in line:
                        # Extract the URL - it's usually in format like:
                        # | https://some-name-xxxx.trycloudflare.com | http://localhost:8888 |
                        match = re.search(r"https://[^\s|]+", line)
                        if match:
                            tunnel_url = match.group(0).strip()
                            break

                    # Also check for URLs without table formatting
                    if "https://" in line:
                        match = re.search(
                            r"https://[^ |\n\r]+\.trycloudflare\.com", line
                        )
                        if match:
                            tunnel_url = match.group(0).strip()
                            break

                    if "error" in line.lower():
                        click.echo(
                            "Error starting Cloudflare tunnel. Please check the logs above."
                        )
                        jupyter_process.terminate()
                        tunnel_process.terminate()
                        sys.exit(1)

                except queue.Empty:
                    # No output for a second, check if process is still alive
                    if tunnel_process.poll() is not None:
                        # Process has ended
                        break
                    continue

            if not tunnel_url:
                click.secho(
                    "Error: Could not get Cloudflare tunnel URL. Exiting.",
                    fg="red",
                    bold=True,
                )
                click.echo(
                    "Try running 'cloudflared tunnel --url http://localhost:8888' manually to check for errors."
                )
                jupyter_process.terminate()
                tunnel_process.terminate()
                sys.exit(1)

            click.secho(f"Cloudflare tunnel created at {tunnel_url}", fg="green")
            
            # Start additional tunnel for app port if specified
            if app_port:
                click.secho(
                    f"Starting additional Cloudflare tunnel for application port {app_port}...", fg="blue", bold=True
                )
                app_cloudflare_cmd = [
                    "cloudflared",
                    "tunnel",
                    "--url",
                    f"http://localhost:{app_port}",
                ]
                
                app_tunnel_process = subprocess.Popen(
                    app_cloudflare_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                )
                
                # Create a queue for the output lines
                app_output_queue = queue.Queue()
                
                # Start reader threads for app tunnel
                threading.Thread(
                    target=reader, args=(app_tunnel_process.stdout, app_output_queue), daemon=True
                ).start()
                threading.Thread(
                    target=reader, args=(app_tunnel_process.stderr, app_output_queue), daemon=True
                ).start()
                
                # Process the output lines
                app_timeout = time.time() + 60  # 60 seconds timeout
                while time.time() < app_timeout:
                    try:
                        line = app_output_queue.get(timeout=1)
                        sys.stdout.write(line)
                        
                        # Look for the cloudflare tunnel URL in both streams
                        if "https://" in line and "trycloudflare.com" in line:
                            match = re.search(r"https://[^\s|]+", line)
                            if match:
                                app_tunnel_url = match.group(0).strip()
                                break
                                
                        # Also check for URLs without table formatting
                        if "https://" in line:
                            match = re.search(
                                r"https://[^ |\n\r]+\.trycloudflare\.com", line
                            )
                            if match:
                                app_tunnel_url = match.group(0).strip()
                                break
                                
                    except queue.Empty:
                        if app_tunnel_process.poll() is not None:
                            break
                        continue
                
                if app_tunnel_url:
                    click.secho(f"Additional Cloudflare tunnel for app port created at {app_tunnel_url}", fg="green")
                else:
                    click.secho(
                        "Warning: Could not create additional tunnel for app port. Continuing without app tunnel.",
                        fg="yellow",
                    )

        # Upload information to dashboard.amdatascience.com if we have an API key
        registered_server_name = None  # Store server name for cleanup later
        if api_key or client:
            click.echo("Uploading information to dashboard.amdatascience.com...")

            try:
                # Import the SDK if needed
                if not client and api_key:
                    from amds import Amds

                    client = Amds(api_key=api_key)

                if client:
                    with client as c:
                        # Create a "server" record with the local Jupyter details
                        server_name = f"local-{int(time.time())}"
                        registered_server_name = server_name  # Save for cleanup
                        environment = "local"

                        # Format data according to the expected API format
                        try:
                            # Add the integrated server using the proper API method
                            request_data = {
                                "environment": environment,
                                "server_name": server_name,
                                "token": token,
                                "url": tunnel_url,
                            }
                            
                            # Add app port forward URL if available
                            if app_tunnel_url:
                                request_data["port_forward_url"] = app_tunnel_url
                                
                            # Add the app port number if available
                            if app_port:
                                request_data["port"] = app_port

                            # Add custom thumbnail if provided, otherwise use default
                            if thumbnail:
                                request_data["thumb"] = thumbnail
                            else:
                                # Use Jupyter's favicon as default thumbnail
                                request_data["thumb"] = (
                                    f"/images/compute_icons/amds.svg"
                                )

                            result = c.integrated_servers.add(request=request_data)

                            click.secho(
                                f"Server registered as '{server_name}'", fg="green"
                            )
                            dashboard_url = "https://dashboard.amdatascience.com"
                            click.echo(
                                f"View in dashboard: {click.style(dashboard_url, fg='bright_blue')}"
                            )
                        except Exception as e:
                            click.echo(
                                f"Warning: Could not register with dashboard: {str(e)}"
                            )
                            registered_server_name = (
                                None  # Reset if registration failed
                            )
                else:
                    click.echo(
                        "Warning: No API key provided. Skipping dashboard integration."
                    )
            except Exception as e:
                click.echo(f"Warning: Failed to connect to dashboard: {str(e)}")
                registered_server_name = None  # Reset if connection failed
        else:
            click.echo(
                "Note: No API key provided. Running without dashboard integration."
            )

        # Open browser if requested
        if not no_browser:
            if registered_server_name:
                full_url = f"https://dashboard.amdatascience.com/alph-editor/{registered_server_name}"
            else:
                full_url = f"{jupyter_url}"

            click.echo(f"Opening browser at {full_url}")
            webbrowser.open(full_url)

        # Format the output based on user preference
        if output_format == "standard":
            click.echo("\n" + "=" * 60)
            click.secho("Jupyter Lab is running", fg="green", bold=True)
            click.echo("=" * 60)
            click.echo("Local URL:     " + click.style(jupyter_url, fg="bright_blue"))
            click.echo("Public URL:    " + click.style(tunnel_url, fg="bright_blue"))
            if app_tunnel_url:
                click.echo("App URL:      " + click.style(app_tunnel_url, fg="bright_blue"))
            if registered_server_name:
                alph_url = f"https://dashboard.amdatascience.com/alph-editor/{registered_server_name}"
                click.echo(
                    "Alph Editor URL: " + click.style(alph_url, fg="bright_blue")
                )
            click.echo("=" * 60)
            click.echo("\nPress Ctrl+C to stop the server...\n")
        elif output_format == "minimal":
            click.echo("Local URL: " + jupyter_url)
            click.echo("Public URL: " + tunnel_url)
            if app_tunnel_url:
                click.echo("App URL: " + app_tunnel_url)
            if registered_server_name:
                alph_url = f"https://dashboard.amdatascience.com/alph-editor/{registered_server_name}"
                click.echo("Alph Editor URL: " + alph_url)
            click.echo("\nPress Ctrl+C to stop the server...")
        elif output_format == "json":
            output = {
                "local_url": jupyter_url,
                "public_url": tunnel_url,
                "token": token,
            }
            if app_tunnel_url:
                output["app_url"] = app_tunnel_url
            if registered_server_name:
                output["alph_url"] = (
                    f"https://dashboard.amdatascience.com/alph-editor/{registered_server_name}"
                )
                output["server_name"] = registered_server_name
            print_json(output)

        # Start health check thread
        def health_checker():
            """Periodically check if services are still running"""
            while True:
                time.sleep(30)  # Check every 30 seconds
                try:
                    # Check if Jupyter is still responsive
                    if not check_jupyter_health(jupyter_url, token):
                        click.secho(
                            "Warning: Jupyter server is not responding! The application may be experiencing issues.",
                            fg="yellow",
                            bold=True,
                        )

                    # Check if tunnel is still connected
                    if not check_tunnel_health(tunnel_url, tunnel_provider):
                        click.secho(
                            f"Warning: {tunnel_provider} tunnel may be down! Public URL may not be accessible.",
                            fg="yellow",
                            bold=True,
                        )
                        
                    # Check app tunnel health if it exists
                    if app_tunnel_url and not check_tunnel_health(app_tunnel_url, tunnel_provider):
                        click.secho(
                            f"Warning: {tunnel_provider} app tunnel may be down! App URL may not be accessible.",
                            fg="yellow",
                            bold=True,
                        )
                except Exception as e:
                    # Log exceptions but don't crash the monitoring thread
                    click.secho(
                        f"Warning: Health check encountered an error: {str(e)}",
                        fg="yellow",
                    )

        # Start health check in a daemon thread
        health_thread = threading.Thread(target=health_checker, daemon=True)
        health_thread.start()

        # Keep the process running until user interrupts
        try:
            jupyter_process.wait()
        except KeyboardInterrupt:
            click.secho("Shutting down...", fg="yellow")
        except Exception as e:
            click.secho(f"Error: {str(e)}", fg="red")
        finally:
            # Clean up processes
            try:
                jupyter_process.terminate()
                click.echo("Jupyter server stopped.")
            except Exception:
                pass

            try:
                tunnel_process.terminate()
                click.echo(f"{tunnel_provider} tunnel closed.")
            except Exception:
                pass
                
            # Clean up app tunnel process if it exists
            if app_port:
                try:
                    if 'app_tunnel_process' in locals():
                        app_tunnel_process.terminate()
                        click.echo(f"{tunnel_provider} app tunnel closed.")
                except Exception:
                    pass

            # Delete the integrated server record if it was registered
            if registered_server_name and (api_key or client):
                click.echo(f"Cleaning up dashboard integration...")
                try:
                    # Import the SDK if needed
                    from amds import Amds

                    # Get the API key - prioritize the directly provided one
                    cleanup_api_key = api_key
                    if not cleanup_api_key and client:
                        # Try to extract API key from client - it might be in a different location
                        # based on the SDK's structure
                        if hasattr(client, "api_key"):
                            cleanup_api_key = client.api_key
                        elif hasattr(client, "sdk_configuration") and hasattr(
                            client.sdk_configuration, "security"
                        ):
                            # Required for ephemeral client in cli
                            cleanup_api_key = client.sdk_configuration.security.api_key
                        elif hasattr(client, "_api_key"):
                            cleanup_api_key = client._api_key
                        else:
                            # Last resort - try to find any attribute that might contain the API key
                            click.echo("Debug - Client attributes: " + str(dir(client)))
                            if hasattr(client, "sdk_configuration"):
                                click.echo(
                                    "Debug - SDK config attributes: "
                                    + str(dir(client.sdk_configuration))
                                )

                    if not cleanup_api_key:
                        click.echo(
                            "Warning: Could not extract API key from client. Using environment variable."
                        )
                        # Try to get from environment
                        import os

                        cleanup_api_key = os.environ.get("AMDS_API_KEY")

                    if cleanup_api_key:
                        # Create a new client without using a context manager
                        cleanup_client = Amds(api_key=cleanup_api_key)
                        # Call delete directly without using a context manager
                        try:
                            result = cleanup_client.integrated_servers.delete(
                                server_name=registered_server_name
                            )
                            click.echo(
                                f"Server '{registered_server_name}' unregistered from dashboard"
                            )
                        except Exception as e1:
                            click.echo(f"Deletion failed: {str(e1)}")
                            click.echo(
                                "The server may need to be manually removed from the dashboard."
                            )
                    else:
                        click.echo(
                            "Warning: No API key available for cleanup. The server may need to be manually removed."
                        )
                except Exception as e:
                    click.echo(
                        f"Warning: Failed to connect to dashboard for cleanup: {str(e)}"
                    )

    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up temporary directory
        try:
            import shutil

            shutil.rmtree(jupyter_dir)
        except Exception:
            pass


def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def find_free_port(start_port, max_attempts=10):
    """Find a free port starting from start_port"""
    port = start_port
    attempts = 0

    while attempts < max_attempts:
        if not is_port_in_use(port):
            return port
        port += 1
        attempts += 1

    return None


def check_jupyter_health(jupyter_url, token):
    """Check if Jupyter server is responding properly"""
    try:
        # Extract base URL without token
        base_url = jupyter_url.split("?")[0]
        # Construct the API URL to check server status
        api_url = f"{base_url}/api/status"
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        response = requests.get(api_url, headers=headers, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def check_tunnel_health(tunnel_url, provider):
    """Check if tunnel is responding properly"""
    try:
        headers = {}
        if provider == "ngrok":
            # Add parameter to bypass ngrok browser warning
            check_url = f"{tunnel_url}?ngrok-skip-browser-warning=true"
            headers["ngrok-skip-browser-warning"] = "true"
        else:
            check_url = tunnel_url

        response = requests.get(check_url, timeout=5, headers=headers)
        return response.status_code < 400
    except Exception:
        return False
