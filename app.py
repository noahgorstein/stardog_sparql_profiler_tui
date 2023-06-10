from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult, events
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Footer, Static, TabPane, TabbedContent
import httpx

from widgets.profiler_panel import ProfilerPanel


class ProfilerApp(App):
    CSS_PATH = "app.css"

    def __init__(
        self,
        auth: httpx.Auth,
        endpoint: str,
        database: str,
        reasoning: bool,
        query: str,
    ):
        self._auth = auth
        self._endpoint = endpoint
        self._database = database
        self._reasoning = reasoning
        self._query = query
        super().__init__()

    BINDINGS = [
        ("p", "show_tab('profiler')", "Profiler"),
        ("q", "show_tab('query')", "Query"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(id="tabs"):
            with TabPane("Profiler", id="profiler"):
                with Vertical():
                    yield ProfilerPanel(
                        id="profiler-panel",
                        auth=self._auth,
                        endpoint=self._endpoint,
                        database=self._database,
                        reasoning=self._reasoning,
                        query=self._query,
                    )
            with TabPane("Query", id="query"):
                with VerticalScroll():
                    s = Syntax(code=self._query, lexer="sparql", line_numbers=True)
                    yield Static(s)
        yield Footer()

    @on(TabbedContent.TabActivated)
    def handle_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Handle TabActivated message sent by TabbedContent."""
        if event.tab.id == "profiler":
            self.get_widget_by_id("plan_node_tree").focus()

    def on_mount(self, event: events.Mount):
        self.get_widget_by_id("plan_node_tree").focus()

    def on_profiler_panel_fatal_error(self, error: ProfilerPanel.FatalError) -> None:
        """If there's a fatal error, just exit and print the error."""
        base_message = "Error profiling query"
        if error.message and error.status_code:
            self.exit(
                f"{base_message} - status code: {error.status_code} - {error.message}"
            )
        elif not error.message and error.status_code:
            self.exit(f"{base_message} - status code: {error.status_code}")
        elif error.message and not error.status_code:
            self.exit(f"{base_message} - {error.message}")
        else:
            self.exit(base_message)

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

        # this is needed to get the bindings to show correctly in footer
        if tab == "profiler":
            self.get_widget_by_id("plan_node_tree").focus()
