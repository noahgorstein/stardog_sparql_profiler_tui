from typing import Optional
from rich.style import Style
from rich.text import Text
from textual.app import RenderResult
from textual.reactive import reactive
from textual.widgets import Static
from widgets import utils

from widgets.plan_tree import PlanNode


class PlanNodeDetails(Static):
    node: reactive[PlanNode | None] = reactive[Optional[PlanNode]](None)

    DEFAULT_CSS = """
    PlanNodeDetails {
        height: 100%;
        background: $panel;
        padding: 1;
    }
    """

    def __init__(self):
        super().__init__()

    def render(self) -> RenderResult:
        if not self.node:
            return ""

        text = [
            (" Node Details \n\n", Style(bgcolor="blue", color="black")),
            *self.generate_details(),
        ]
        return Text.assemble(*text)

    def generate_details(self) -> list[str | tuple[str, str]]:
        """
        Generate a list of details about a node, including its label, cardinality, memory usage,
        results, and wall time.

        Returns:
            list[str | tuple[str, str]]: A list containing details as strings or tuples of
            (detail text, style) where style can be used for formatting in the output.
        """
        details: list[str | tuple[str, str]] = []
        if not self.node:
            return details

        label = self.node.label
        cardinality = self.node.cardinality
        memory = self.node.memory
        results = self.node.results
        gaps = self.node.gaps
        time = self.node.time_ms

        if label:
            if utils.is_pipeline_breaker(label):
                details.append(("💥", ""))
            details.append((f"{label}\n\n", ""))

        if cardinality:
            details.append(("Cardinality: ", "bold blue"))
            details.append((f"{cardinality}\n\n", ""))

        if memory:
            details.append(("Memory: ", "bold blue"))
            details.append((f"{memory}\n\n", ""))

        if results:
            details.append(("Results: ", "bold blue"))
            details.append((f"{results}", ""))
            if gaps:
                details.append((" (with gaps)", "italic"))
            details.append(("\n\n", ""))

        if isinstance(time, int):
            details.append(("Wall Time: ", "bold blue"))
            details.append((f"{time}ms\n\n", ""))

        return details
