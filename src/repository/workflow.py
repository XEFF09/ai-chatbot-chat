from typing_extensions import Protocol
from langgraph.graph.state import CompiledStateGraph


class Workflow(Protocol):
    def _build_workflow(self) -> CompiledStateGraph: ...
    def get_graph(self) -> CompiledStateGraph: ...
