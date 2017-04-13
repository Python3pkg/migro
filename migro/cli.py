#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import click

from . import __version__, main

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.argument('directory')
def init(directory):
    """Create new scripts directory and a configuration file"""
    main.init(directory)


@cli.command()
@click.option('-c', '--config', default='migro.yaml',
              help='Alternate config file', type=click.Path(exists=True))
def current(config):
    """Display current revision"""
    with open(config, 'r'):
        main.current(yaml.load(open(config)))


@cli.command()
@click.argument('message')
@click.option('-c', '--config', default='migro.yaml',
              help='Alternate config file', type=click.Path(exists=True))
def revision(config, message):
    """Create new revision file in a scripts directory"""
    with open(config, 'r'):
        main.revision(yaml.load(open(config)), message)


@cli.command()
@click.argument('rev', metavar='<rev>')
@click.option('-c', '--config', default='migro.yaml',
              help='Alternate config file', type=click.Path(exists=True))
def checkout(config, rev):
    """Upgrade/revert to a different revision.
    
    <rev> must be "head", integer or revision id. To pass negative
    number you need to write "--" before it"""
    with open(config, 'r'):
        main.checkout(yaml.load(open(config)), rev)


@cli.command()
@click.option('-c', '--config', default='migro.yaml',
              help='Alternate config file', type=click.Path(exists=True))
def reapply(config):
    """Reapply current revision"""
    with open(config, 'r'):
        main.reapply(yaml.load(open(config)))


@cli.command()
@click.option('-c', '--config', default='migro.yaml',
              help='Alternate config file', type=click.Path(exists=True))
def show(config):
    """Show revision list"""
    with open(config, 'r'):
        main.show(yaml.load(open(config)))
