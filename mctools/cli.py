import os
import sys
import click


class Context(object):

    def __init__(self):
        self.debug = False
        self.quiet = False
        self.sickrage_api_key = 'fa0adbb947531e91266a7a8bd7cbc3d7'
        self.couchpotato_api_key = '60891312ece04977a59772392bb0f745'

    def log(self, msg, lvl='info'):
        """Logs a message to stderr."""
        if not self.quiet:
            if lvl in ['i', 'info']:
                click.echo(msg, file=sys.stdout)
            elif lvl in ['e', 'error']:
                click.echo(msg, file=sys.stderr)
            elif lvl in ['w', 'warn']:
                click.echo(msg, file=sys.stderr)
            elif lvl in ['s', 'start']:
                click.echo(msg, file=sys.stdout)
            elif lvl in ['n', 'end']:
                click.echo(msg, file=sys.stdout)
            elif lvl in ['d', 'debug']:
                if self.debug:
                    click.echo(msg, file=sys.stdout)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__(
                'mctools.mctools.commands.cmd_' + name,
                None,
                None,
                ['cli']
             )
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
@click.option('-d', '--debug',
              is_flag=True,
              help="Enables debug mode.")
@click.option('-q', '--quiet',
              is_flag=True,
              help="Enables quiet mode")
@pass_context
def cli(ctx, debug, quiet):
    """mctools command line interface."""
    ctx.debug = debug
    ctx.quiet = quiet
