"""
Command-line interface for image tag helper.
"""
import click
from .core import get_image_tag_by_short_name
from .config import config


@click.group()
def cli():
    """Image Tag Helper - Find the latest image tag based on a short name."""
    pass


@cli.command()
@click.option("--tag", "-t", default="master-latest", help="Short tag name")
@click.option("--arch", "-a", default="amd64", help="Architecture (amd64, arm64, etc)")
@click.option("--registry", "-r", help="Registry URL")
@click.option("--repository", "-p", help="Repository path (project/repo)")
@click.option("--profile", "-f", help="Use a predefined registry profile")
@click.option("--quiet", "-q", is_flag=True, help="Only output the tag")
def get_tag(tag, arch, registry, repository, profile, quiet):
    """Get the full image tag by short name."""
    # If profile is provided, use it to get registry and repository
    if profile:
        profile_registry, profile_repository = config.get_alias(profile)
        if profile_registry and profile_repository:
            registry = profile_registry
            repository = profile_repository
            if not quiet:
                click.echo(f"Using registry profile '{profile}': {registry}/{repository}", err=True)
        else:
            if not quiet:
                click.echo(f"Registry profile '{profile}' not found. Using default or provided values.", err=True)
    # If no profile provided, try to use default profile
    elif not (registry and repository):
        default_registry, default_repository = config.get_default_profile()
        if default_registry and default_repository:
            registry = default_registry
            repository = default_repository
            if not quiet:
                click.echo(f"Using default profile: {registry}/{repository}", err=True)
    
    # Use defaults if not provided
    registry = registry or "harbor.milvus.io"
    repository = repository or "milvus/milvus"
    
    result = get_image_tag_by_short_name(tag, arch, registry, repository)
    click.echo(result)


@cli.group()
def registry():
    """Manage registry configurations."""
    pass


@registry.command("add")
@click.argument("name")
@click.option("--registry", "-r", required=True, help="Registry URL")
@click.option("--repository", "-p", required=True, help="Repository path (project/repo)")
def add_registry(name, registry, repository):
    """Add a registry configuration."""
    config.set_alias(name, registry, repository)
    click.echo(f"Registry '{name}' added: {registry}/{repository}")


@registry.command("remove")
@click.argument("name")
def remove_registry(name):
    """Remove a registry configuration."""
    if config.remove_alias(name):
        click.echo(f"Registry '{name}' removed")
    else:
        click.echo(f"Registry '{name}' not found")


@registry.command("list")
def list_registries():
    """List all registry configurations."""
    aliases = config.list_aliases()
    if not aliases:
        click.echo("No registry configurations defined")
        return
    
    click.echo("Defined registry configurations:")
    for name, details in aliases.items():
        is_default = "(default)" if name == config.default_profile else ""
        click.echo(f"  {name}{is_default}: {details['registry']}/{details['repository']}")


@registry.command("set-default")
@click.argument("name")
def set_default_registry(name):
    """Set a registry configuration as default."""
    if config.set_default_profile(name):
        click.echo(f"Registry '{name}' set as default")
    else:
        click.echo(f"Registry '{name}' not found")


if __name__ == "__main__":
    cli()
