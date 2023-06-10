from typing import Optional

from rich.text import Text
from textual.app import RenderResult
from textual.reactive import reactive
from textual.widgets import Static


class ProfilerStats:
    def __init__(self, profiler_stats: dict):
        self.total_memory = profiler_stats.get("memory")
        self.time = int(profiler_stats.get("time", 0))
        self.time_unit = profiler_stats.get("time unit")
        self.results = profiler_stats.get("results")

        if self.time_unit == "s":
            self.time_ms = self.time * 1000
        elif self.time_unit == "m":
            self.time_ms = self.time * 60 * 1000
        else:
            self.time_ms = self.time




class ProfilerDetails(Static):
    SPACER = "  •  "

    stats: reactive[ProfilerStats | None] = reactive[Optional[ProfilerStats]](None)

    def __init__(self, id: str):
        super().__init__(id=id)

    def render(self) -> RenderResult:
        if self.stats is not None:
            return Text.assemble(*self.format())
        else:
            return ""

    def format(self) -> list[tuple[str, str] | str]:
        if not self.stats:
            return []

        details: list[tuple[str, str] | str] = []
        if self.stats.results:
            details.append(("Results: ", "bold"))
            details.append(f"{self.stats.results}")
            details.append(self.SPACER)
        if self.stats.total_memory:
            details.append(("Total Memory: ", "bold"))
            details.append(f"{self.stats.total_memory}")
            details.append(self.SPACER)
        if self.stats.time:
            details.append(("Execution Time: ", "bold"))
            details.append(f"{self.stats.time}{self.stats.time_unit}\n")

        return details
