from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState as State, START, END
from langgraph.graph.state import CompiledStateGraph
from repository.workflow import Workflow
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field


class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )


class LilianwengWorkflow(Workflow):
    def __init__(self, generate_model, grade_model, tools):
        self.tools = tools
        self.generate_model = generate_model.bind_tools(tools)
        self.grade_model = grade_model
        self.workflow = self._build_workflow()
        self.GRADE_PROMPT = (
            "You are a grader assessing relevance of a retrieved document to a user question. \n "
            "Here is the retrieved document: \n\n {context} \n\n"
            "Here is the user question: {question} \n"
            "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
            "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
        )
        self.REWRITE_PROMPT = (
            "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
            "Here is the initial question:"
            "\n ------- \n"
            "{question}"
            "\n ------- \n"
            "Formulate an improved question:"
        )
        self.GENERATE_PROMPT = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Use three sentences maximum and keep the answer concise.\n"
            "Question: {question} \n"
            "Context: {context}"
        )

    def _build_workflow(self):
        builder = StateGraph(State)

        builder.add_node("gen_query_or_respond_node", self.gen_query_or_respond_node)
        builder.add_node("rewrite_question_node", self.rewrite_question_node)
        builder.add_node("gen_ans_node", self.gen_ans_node)
        builder.add_node("retrieve_node", ToolNode(self.tools))

        builder.add_edge(START, "gen_query_or_respond_node")
        builder.add_conditional_edges(
            "gen_query_or_respond_node",
            tools_condition,
            {
                "tools": "retrieve_node",
                END: END,
            },
        )
        builder.add_conditional_edges(
            "retrieve_node",
            self.grade_doc_activator,
        )
        builder.add_edge("gen_ans_node", END)
        builder.add_edge("rewrite_question_node", "gen_query_or_respond_node")

        return builder.compile()

    async def gen_query_or_respond_node(self, state: State):
        res = await self.generate_model.ainvoke(state["messages"])
        return {"messages": [res]}

    async def grade_doc_activator(self, state: State):
        """Determine whether the retrieved documents are relevant to the question."""
        question = state["messages"][0].content
        context = state["messages"][-1].content

        prompt = self.GRADE_PROMPT.format(question=question, context=context)
        response = await self.grade_model.with_structured_output(
            GradeDocuments
        ).ainvoke([{"role": "user", "content": prompt}])
        score = response.binary_score

        if score == "yes":
            return "gen_ans_node"
        else:
            return "rewrite_question_node"

    async def rewrite_question_node(self, state: State):
        """Rewrite the original user question."""
        messages = state["messages"]
        question = messages[0].content
        prompt = self.REWRITE_PROMPT.format(question=question)
        response = self.generate_model.invoke([{"role": "user", "content": prompt}])
        return {"messages": [HumanMessage(content=response.content)]}

    def gen_ans_node(self, state: State):
        """Generate an answer."""
        question = state["messages"][0].content
        context = state["messages"][-1].content
        prompt = self.GENERATE_PROMPT.format(question=question, context=context)
        response = self.generate_model.invoke([{"role": "user", "content": prompt}])
        return {"messages": [response]}

    def get_graph(self) -> CompiledStateGraph:
        return self.workflow
