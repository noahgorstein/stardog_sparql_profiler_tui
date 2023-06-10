import click
import httpx
import app


class TokenAuth(httpx.Auth):
    """Handles bearer/token auth"""

    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-u",
    "--username",
    default="admin",
    show_default=True,
    help="Stardog username (applicable only if token not provided)",
    type=click.STRING,
)
@click.option(
    "-p",
    "--password",
    default="admin",
    show_default=True,
    help="Stardog password (applicable only if token not provided)",
    type=click.STRING,
)
@click.option(
    "-t",
    "--token",
    show_default=True,
    help="Auth JWT token (applicable only if username and password are not provided)",
    type=click.STRING,
)
@click.option(
    "-e",
    "--endpoint",
    required=True,
    default="http://localhost:5820",
    show_default=True,
    help="Stardog endpoint",
    type=click.STRING,
)
@click.option(
    "-d", "--database", required=True, help="Stardog database", type=click.STRING
)
@click.option(
    "-r",
    "--reasoning",
    required=False,
    default=False,
    is_flag=True,
    help="Enables reasoning for the query to be profiled.",
)
@click.option(
    "-f",
    "--query_file",
    required=False,
    help="File containing query to profile",
    type=click.File("r"),
)
@click.argument("query", required=False)
def query_profiler_app(
    username: str,
    password: str,
    token: str,
    endpoint: str,
    database: str,
    reasoning: bool,
    query_file: click.File,
    query: str,
):
    """Profiles the QUERY.

    If both the query_file option and QUERY argument are provided, the QUERY argument
    will take precedence.

    If token is provided in addition to a username and password for authentication, the token
    will take precedence.
    """
    if (not username and not password) and not token:
        raise click.UsageError("Please provide either username and password or token.")

    query_to_profile = query
    if query_file is not None:
        query_to_profile = query_file.read() # type: ignore

    if query_to_profile is None:
        raise click.UsageError(
            "Please provide a file containing a query or the query as an argument."
        )

    auth = (
        TokenAuth(token=token)
        if token
        else httpx.BasicAuth(username=username, password=password)
    )

    profiler_app = app.ProfilerApp(
        auth=auth,
        query=query_to_profile,
        database=database,
        reasoning=reasoning,
        endpoint=endpoint,
    )
    exit_message = profiler_app.run()
    if exit_message:
        print(exit_message)
