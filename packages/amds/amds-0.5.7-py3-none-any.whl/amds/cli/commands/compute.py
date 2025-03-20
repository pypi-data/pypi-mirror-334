import click
from ..utils import print_json

@click.group()
def compute():
    """Manage compute resources"""
    pass

@compute.command('list')
@click.pass_obj
def list_compute(client):
    """List compute information"""
    with client as c:
        res = c.compute.get()

        result = res.result
        
        if not result.compute:
            click.echo("No compute resources found.")
            return
            
        click.echo("\nAvailable Compute Resources:")
        click.echo("─" * 75)
        
        for comp in result.compute:
            click.echo(f"Name:         {click.style(comp.name, fg='bright_green')}")
            click.echo(f"Host:         {comp.cloud_host}")
            if hasattr(comp, "memory"):
                click.echo(f"Memory:       {comp.memory}")
            if hasattr(comp, "cpus"):
                click.echo(f"CPUs:         {comp.cpus}")
            if hasattr(comp, "num_gpus"):
                click.echo(f"GPUs:         {comp.num_gpus}")
            if hasattr(comp, "vram_per_gpu") and comp.vram_per_gpu != "0G":
                click.echo(f"VRAM/GPU:     {comp.vram_per_gpu}")
            if hasattr(comp, "total_vram") and comp.total_vram != "0G":
                click.echo(f"Total VRAM:   {comp.total_vram}")
            if hasattr(comp, "hourly_price"):
                click.echo(f"Hourly Price: ${comp.hourly_price}")
                
            # Display availability information
            if hasattr(comp, "availability") and comp.availability:
                click.echo("Availability: ")
                for region in comp.availability:
                    status = click.style("Available", fg="green") if region.available else click.style("Unavailable", fg="red")
                    click.echo(f"  - {region.region}: {status}")
                    
            click.echo("─" * 75) 

@compute.command('get')
@click.option("--compute-id", required=True, help="ID of the compute resource")
@click.pass_obj
def get_compute(client, compute_id):
    """Get details of a specific compute resource by name"""
    with client as c:
        res = c.compute.get()
        result = res.result
        
        if not result.compute:
            click.echo("No compute resources found.")
            return
            
        compute = next((comp for comp in result.compute if comp.compute_id== compute_id), None)
        
        if compute:
            click.echo("\nCompute Resource Details:")
            click.echo("─" * 75)
            click.echo(f"Name:         {click.style(compute.name, fg='bright_green')}")
            click.echo(f"Host:         {compute.cloud_host}")
            if hasattr(compute, "memory"):
                click.echo(f"Memory:       {compute.memory}")
            if hasattr(compute, "cpus"):
                click.echo(f"CPUs:         {compute.cpus}")
            if hasattr(compute, "num_gpus"):
                click.echo(f"GPUs:         {compute.num_gpus}")
            if hasattr(compute, "vram_per_gpu") and compute.vram_per_gpu != "0G":
                click.echo(f"VRAM/GPU:     {compute.vram_per_gpu}")
            if hasattr(compute, "total_vram") and compute.total_vram != "0G":
                click.echo(f"Total VRAM:   {compute.total_vram}")
            if hasattr(compute, "hourly_price"):
                click.echo(f"Hourly Price: ${compute.hourly_price}")
                
            # Display availability information
            if hasattr(compute, "availability") and compute.availability:
                click.echo("Availability: ")
                for region in compute.availability:
                    status = click.style("Available", fg="green") if region.available else click.style("Unavailable", fg="red")
                    click.echo(f"  - {region.region}: {status}")
                    
            click.echo("─" * 75)
        else:
            click.echo(f"Compute resource '{name}' not found", err=True) 