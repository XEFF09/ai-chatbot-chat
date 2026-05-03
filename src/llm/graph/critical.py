from langchain.agents import create_agent
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from llm.model import model
from llm.prompt.critical import SYSTEM_PROMPT

critical_agent = create_agent(model=model, tools=[], system_prompt=SYSTEM_PROMPT)


class State(TypedDict):
    reqMessage: str
    draft: str
    review: str


async def write_node(state: State):
    prompt = f"Answer this question: {state['reqMessage']}"
    res = await model.ainvoke([{"role": "user", "content": prompt}])
    return {"draft": res.content}


async def review_node(state: State):
    draft = state.get("draft")
    prompt = f"Review the following text and provide feedback: {draft}"
    res = await model.ainvoke([{"role": "user", "content": prompt}])
    return {"review": res.content}


workflow = StateGraph(State)

workflow.add_node("writer", write_node)
workflow.add_node("reviewer", review_node)

workflow.set_entry_point("writer")
workflow.add_edge("writer", "reviewer")
workflow.add_edge("reviewer", END)

critical_graph = workflow.compile()
