import httpx
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widget import Widget
from textual.widgets import LoadingIndicator
from textual.worker import Worker, WorkerState
from widgets.plan_node_details import PlanNodeDetails

from widgets.plan_tree import PlanNode, PlanNodeTree
from widgets.profiler_details import ProfilerDetails, ProfilerStats


def sum_wall_time(node: PlanNode) -> int:
    if node.children == 0:
        return 0

    total_time = 0
    for child in node.children:
        child_time = child.time_ms or 0  # Consider None as 0
        total_time += child_time + sum_wall_time(node=child)

    return total_time


class ProfilerPanel(Widget):
    BINDINGS = [("t", "show_node_details()", "Toggle Details")]

    DEFAULT_CSS = """

     #tree-content {
        layout: grid;
        grid-size: 2;
        grid-columns: 3fr 1fr;
     }

     #tree-content.no-side-panel {
        layout: grid;
        grid-size: 1;
        grid-columns: 1fr;
    }

    """

    def __init__(
        self,
        id: str,
        auth: httpx.Auth,
        endpoint: str,
        database: str,
        reasoning: bool,
        query: str,
    ):
        super().__init__(id=id)
        self._auth = auth
        self._endpoint = endpoint
        self._database = database
        self._reasoning = reasoning
        self._query = query

    class FatalError(Message):
        """Fatal Error message"""

        def __init__(self, message: str | None = None, status_code: int | None = None):
            self.message = message
            self.status_code = status_code
            super().__init__()

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        with Container(id="profiler-panel"):
            yield ProfilerDetails(id="profiler-details")
            with Container(id="tree-content"):
                yield PlanNodeTree(
                    id="plan_node_tree",
                    label="root",
                    data=PlanNode(plan_node_dict={}),
                    query_plan={},
                    namespaces={},
                )
                yield PlanNodeDetails()

    def on_mount(self) -> None:
        tree = self.query_one(PlanNodeTree)
        tree.display = False
        self.fetch_query_profile()

    def action_show_node_details(self) -> None:
        container = self.get_widget_by_id("tree-content")
        details = self.query_one(PlanNodeDetails)
        container.toggle_class("no-side-panel")
        if details.display:
            details.display = False
        else:
            details.display = True

    @on(PlanNodeTree.NodeHighlighted)
    def handle_plan_node_tree_node_highlighted(
        self, event: PlanNodeTree.NodeHighlighted[PlanNode]
    ):
        """Handles what to do each time a node in the tree is highlighted. """
        details = self.query_one(PlanNodeDetails)
        details.node = event.node.data

    def setup(self, response: dict) -> None:
        """
        Initializes the ProfilerPanel given the JSON response from the profiler endpoint.
        """

        self.query_one(LoadingIndicator).display = False

        profiler_details = self.query_one(ProfilerDetails)
        profiler_details.stats = ProfilerStats(profiler_stats=response["profiler"])

        tree = self.query_one(PlanNodeTree)
        tree.set_profiler_stats(response["profiler"])
        tree.namespaces = response["prefixes"]
        tree.build(query_plan=response["plan"])

        p = PlanNode(plan_node_dict=response["plan"])

        root = tree.root
        root.label, root.data = p.label, p
        root.expand_all()
        tree.display = True

        self.query_one(PlanNodeDetails).node = root.data

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.ERROR:
            exception = event.worker.error
            if isinstance(exception, httpx.HTTPStatusError):
                try:
                    error = exception.response.json()
                except Exception:
                    pass

                error_message = error["message"] if error is not None else None
                self.post_message(
                    self.FatalError(
                        message=error_message,
                        status_code=exception.response.status_code,
                    )
                )
            elif isinstance(exception, httpx.ConnectError):
                self.post_message(
                    self.FatalError(
                        message=f"Unable to establish a connection to Stardog endpoint: {self._endpoint}"
                    )
                )
            else:
                self.post_message(self.FatalError(message=str(exception)))

    @work(exit_on_error=False) # type: ignore
    async def fetch_query_profile(self) -> None:
        """Get the profiled query from Stardog.

        Stardog HTTP API: https://stardog-union.github.io/http-docs/#tag/SPARQL/operation/explainQueryGet
        """

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self._endpoint}/{self._database}/explain",
                params=[
                    ("profile", True),
                    ("query", self._query),
                    ("reasoning", self._reasoning),
                ],
                headers={"Accept": "application/json"},
                auth=self._auth,
            )
            resp.raise_for_status()

            self.setup(response=resp.json())
