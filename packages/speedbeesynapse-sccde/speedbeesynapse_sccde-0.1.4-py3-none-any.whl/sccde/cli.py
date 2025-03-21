"""SpeeDBeeSynapse custom component development environment tool."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from .main import Sccde

PACKAGE_SUFFIX = '.sccpkg'


@click.group()
def cli() -> None:
    """Make subcommand group."""


@cli.command()
@click.argument('target_dir', required=False, type=click.Path(file_okay=False, dir_okay=True, path_type=Path))
def init(target_dir: Optional[Path]) -> None:
    """Initialize directory."""
    sccde = Sccde(target_dir if target_dir else Path())
    sccde.init('Custom component package example')
    sccde.add_sample('python', 'collector')


@cli.command()
@click.option('-C', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option('-l', '--sample-language', default='python', type=click.Choice(['c', 'python']))
@click.option('-t', '--sample-type', default='collector', type=click.Choice(['collector', 'serializer', 'emitter']))
def add(c: Path, sample_language: str, sample_type: str) -> None:
    """Add sample component."""
    sccde = Sccde(c)
    sccde.add_sample(sample_language, sample_type)


@cli.command()
@click.option('-C', default=Path(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option('-o', '--out', type=click.Path(path_type=Path))
def make_package(c: Path, out: Optional[Path]) -> None:
    """Make package."""
    out = out.with_suffix(PACKAGE_SUFFIX) if out else None
    sccde = Sccde(c)
    sccde.make_package(out)


@cli.command()
def serve() -> None:
    """Start test server."""


if __name__ == '__main__':
    cli()
