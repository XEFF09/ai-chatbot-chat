from langchain.tools import tool

from repository.tool_set import ToolSet


class LiliangwengToolSet(ToolSet):
    def __init__(self, store):
        self.store = store

    def get_tools(self):
        @tool
        async def retriever_tool(query: str) -> str:
            """Search and return information about Lilian Weng blog posts."""
            retriever = self.store.as_retriever()
            docs = await retriever.ainvoke(query)
            return "\n\n".join([doc.page_content for doc in docs])

        return [retriever_tool]
