import os
import sys
import click
import yaml


class Context(object):

    def __init__(self):
        self.debug = False
        self.quiet = False
        self.config = None
        self.credentials = None
        self.sickrage = None
        self.couchpotato = None

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

    def set_credential_and_config(self, credential_file):
        """Sets various credentials"""
        with open(credential_file, 'r') as f:
            file = yaml.load(f.read())

        self.credentials = file['credentials']
        self.config = file['config']


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
@click.option('-c', '--credential-file',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              default=os.path.expanduser(os.environ.get("MCTOOLS_CREDENTIALS", "~/.mctools.yml")),
              help="Credentials file for mctools to use to communicate with various APIs")
@pass_context
def cli(ctx, debug, quiet, credential_file):
    """mctools command line interface."""
    ctx.debug = debug
    ctx.quiet = quiet
    if credential_file:
        ctx.set_credential_and_config(credential_file)
    else:
        click.echo("Credential File must be defined")
        sys.exit(1)
