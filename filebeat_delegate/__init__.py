# coding=utf8

import click
from server import Server
from parser import Configure



@click.group()
def cli():
    pass


@click.command()
@click.option('-c', '--config', default='', help='file path of config file')
def test(config):
    try:
        Configure.instance().parse(config)
    except AssertionError as e:
        click.echo(u"Parse ERRORS:%s" % e)
    except IOError as e:
        click.echo(u'Configure file %s not found' % config)


@click.command()
@click.option('-c', '--config', default='', help='file path of config file')
def export(config):
    try:
        Configure.instance().export_config(config)
        click.echo('Configuration exported to %s' % config)
    except IOError as e:
        click.echo(e.message)


@click.command()
@click.option('-c', '--config', default='', help='file path of config file')
def watch(config):
    try:
        Configure.instance().parse(config)
        click.echo('Watcher is starting...')
        Server.instance().start(Configure.instance())
    except IOError as e:
        click.echo(e.message)



def main():
    cli.add_command(test)
    cli.add_command(export)
    cli.add_command(watch)
    cli()


if __name__ == '__main__':
    main()
