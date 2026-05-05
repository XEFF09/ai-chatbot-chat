from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from repository.workflow import Workflow


class State(TypedDict):
    req_message: str
    draft: str
    review: str


class CriticalWorkflow(Workflow):
    def __init__(self, model):
        self.model = model
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> CompiledStateGraph:
        builder = StateGraph(State)

        builder.add_node("writer", self.write_node)
        builder.add_node("reviewer", self.review_node)

        builder.set_entry_point("writer")
        builder.add_edge("writer", "reviewer")
        builder.add_edge("reviewer", END)

        return builder.compile()

    async def write_node(self, state: State):
        prompt = f"Answer this question: {state['req_message']}"
        res = await self.model.ainvoke([{"role": "user", "content": prompt}])
        return {"draft": res.content}

    async def review_node(self, state: State):
        draft = state.get("draft")
        prompt = f"Review the following text: {draft}"
        res = await self.model.ainvoke([{"role": "user", "content": prompt}])
        return {"review": res.content}

    def get_graph(self) -> CompiledStateGraph:
        return self.workflow
