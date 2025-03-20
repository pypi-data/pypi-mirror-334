# AMDS CLI Commands

This directory contains the command modules for the American Data Science CLI.

## Available Commands

- `environments`: Manage environments
- `servers`: Manage servers
- `compute`: Manage compute resources
- `login`: Authenticate with American Data Science API
- `jupyter`: Manage local Jupyter Lab instances (new)

## Jupyter Command

The `jupyter` command allows you to launch a local Jupyter Lab instance with advanced features:

- Automatically configures a public URL via ngrok
- Uploads instance information to dashboard.amdatascience.com
- Option to launch with alph-editor extension
- Password protection for Jupyter server
- Custom ngrok configuration including regional endpoints and authentication
- Automatic port conflict resolution
- Health monitoring for Jupyter and ngrok services

### Prerequisites

- Jupyter Lab installed: `pip install jupyterlab`
- ngrok installed: Download from [ngrok.com](https://ngrok.com/download)
- (Optional) alph-editor extension for Jupyter Lab

### Usage

```bash
# Launch a basic Jupyter Lab instance
amds jupyter launch

# Launch with alph-editor
amds jupyter launch --with-alph

# Specify a custom port and directory
amds jupyter launch --port 9999 --directory /path/to/notebooks

# Launch with password protection
amds jupyter launch --password "your-secure-password"

# Launch with ngrok authentication
amds jupyter launch --ngrok-auth "username:password"

# Launch with a specific ngrok region
amds jupyter launch --ngrok-region eu

# Specify a custom thumbnail URL for dashboard display
amds jupyter launch --thumbnail "https://example.com/custom-thumbnail.png"

# Use JSON output format for scripting
amds jupyter launch --output-format json

# Launch without opening browser
amds jupyter launch --no-browser
```

### Options

- `--port`: Port to run Jupyter Lab on (default: 8888)
- `--no-browser`: Don't open browser automatically
- `--with-alph`: Launch with alph-editor extension
- `--directory`: Directory to launch Jupyter Lab in (default: current directory)
- `--ngrok-port`: Port for ngrok to use (defaults to same as Jupyter port)
- `--ngrok-domain`: Domain for ngrok to use (required for Pay-as-you-go plans)
- `--ngrok-auth`: Basic authentication for ngrok tunnel (format: username:password)
- `--ngrok-region`: Region for ngrok tunnel (us, eu, ap, au, sa, jp, in)
- `--api-key`: API key for dashboard integration
- `--allow-origin`: CORS allow-origin setting (default: *)
- `--disable-sudo`: Disable sudo/root permissions in the notebook
- `--password`: Set a password for Jupyter Lab
- `--output-format`: Output format (standard, minimal, json)
- `--thumbnail`: Custom thumbnail URL for dashboard display (defaults to Jupyter favicon)

### Features

#### Automatic Port Detection

The command automatically detects if ports are already in use and finds available alternatives.

#### Health Monitoring

Background monitoring ensures Jupyter and ngrok services remain operational, with warnings if issues are detected.

#### Colorized Output

Terminal output uses colors to highlight important information and make status updates more visible.

#### Multiple Output Formats

Choose between standard (colorized, formatted output), minimal (text only, good for logs), or JSON (for script consumption). 