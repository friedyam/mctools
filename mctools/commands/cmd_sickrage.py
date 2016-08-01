import click
from mctools.mctools.cli import pass_context
from mctools.utils.sickrage import SickRage


@click.group(name='sickrage', help="General SickRage Interface")
@click.option('-p', '--port',
              type=int,
              help="Port that SickRage is listening to")
@pass_context
def cli(ctx, port):
    ctx.sickrage = SickRage(ctx.base_url, ctx.sickrage_port, ctx.sickrage_api_key)


@cli.command('shows', short_help="Lists the available shows")
@pass_context
def shows(ctx):
    shows = ctx.sickrage.list_shows()
    for show in shows:
        print(show.name)


@cli.command('postprocess',
             short_help="Starts the postprocessor in a given directory")
@click.option('--dir',
              help="The directory you want the postprocessor to check")
@pass_context
def postprocess(ctx, dir):
    click.echo("Starting Post-Process")
    result = ctx.sickrage.post_process()
    click.echo("Post-Processing is {0}".format(result))


@cli.command('schedule',
             short_help="Shows upcoming Show Schedule")
@click.option('-t', '--today',
              is_flag=True,
              help="Only displays shows on today")
@pass_context
def schedule(ctx, today):
    if today:
        schedule = ctx.sickrage.future(type=('today',))
    else:
        schedule = ctx.sickrage.future()

    click.echo()
    for day in schedule:
        click.secho(day + ':', fg='yellow', bold=True)
        for s in schedule[day]:
            click.echo(s.show_name + ' ' + click.style(s.airdate.strftime("%I:%M %p"), fg='white'))
        click.echo()


@cli.command('stats',
             short_help="Show Statistics")
@pass_context
def stats(ctx):
    color = 'white'
    stats = ctx.sickrage.shows_stats()
    click.echo("Number of Downloaded Episodes: " + click.style(str(stats.episodes_downloaded), fg=color))
    click.echo("  Number of Snatched Episodes: " + click.style(str(stats.episodes_snatched), fg=color))
    click.echo("     Total Number of Episodes: " + click.style(str(stats.total_episodes), fg=color))
    click.echo("       Number of Active Shows: " + click.style(str(stats.active_shows), fg=color))
    click.echo("        Total Number of Shows: " + click.style(str(stats.total_shows), fg=color))


@cli.command('restart',
             short_help="Restart Sickrage")
@pass_context
def restart(ctx):
    restart = ctx.sickrage.restart()
    if restart == "success":
        click.echo("Restarted")
    else:
        click.echo("Error restarting")


@cli.command('show',
             short_help="Displays a shows information")
@click.argument('name')
@pass_context
def show(ctx, name):
    color = 'white'
    try:
        show = ctx.sickrage.show(name)
    except KeyError:
        click.echo("Incorrect show name")
    else:
        click.echo("   Show Name: " + click.style(show.name, fg=color))
        click.echo("      Status: " + click.style(show.status, fg=color))
        click.echo("        Airs: " + click.style(show.airs, fg=color))
        click.echo("Next Episode: " + click.style(show.next_episode, fg=color))
        click.echo("     Network: " + click.style(show.network, fg=color))
        click.echo("    Genre(s): " + click.style(', '.join(show.genres), fg=color))
        click.echo("    Location: " + click.style(show.location, fg=color))
        click.echo("   Indexerid: " + click.style(str(show.indexerid), fg=color))
