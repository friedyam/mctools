import click
from mctools.mctools.cli import pass_context
from mctools.utils.couchpotato import CouchPotato


@click.group('couchpotato', short_help="General CouchPotato Interface")
@click.option('-p', '--port',
              type=int,
              help="Port that SickRage is listening to")
@pass_context
def cli(ctx, port):
    ctx.couchpotato = CouchPotato(ctx.config['base_url'], ctx.config['couchpotato_port'], ctx.credentials['couchpotato']['api_key'])


@cli.command('restart', short_help="Restarts CouchPotato")
@pass_context
def restart(ctx):
    restart = ctx.couchpotato.restart()
    click.echo(restart)


@cli.command('renamer', short_help="Kicks off renamer scan")
@pass_context
def renamer(ctx):
    resp = ctx.couchpotato.renamer()
    click.echo(resp)


@cli.command('movies', short_help="Displays List of Movies")
@click.option('-n', '--name',
              type=str,
              default=None,
              help="Search string to match movie names against")
@pass_context
def movies(ctx, name):
    movies = ctx.couchpotato.list_movies(search=name)
    for movie in movies:
        click.echo(movie.title)
