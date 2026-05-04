from langgraph.graph import StateGraph, MessagesState as State
from langgraph.graph.state import CompiledStateGraph
from repository.workflow import Workflow
from langgraph.prebuilt import ToolNode, tools_condition


class RagWorkflow(Workflow):
    def __init__(self, model, tools=[]):
        self.model = model
        self.tools = tools
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        builder = StateGraph(State)

        builder.add_node("query_or_respond_node", self.query_or_respond_node)
        builder.add_node("tools", ToolNode(self.tools))

        builder.set_entry_point("query_or_respond_node")
        builder.add_conditional_edges(
            "query_or_respond_node",
            tools_condition,
        )
        builder.add_edge("tools", "query_or_respond_node")

        return builder.compile()

    async def query_or_respond_node(self, state: State):
        res = await self.model.bind_tools(self.tools).ainvoke(state["messages"])
        return {"messages": [res]}

    def get_graph(self) -> CompiledStateGraph:
        return self.workflow
