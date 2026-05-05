from langchain_core.messages import HumanMessage
from repository.agent import AgentRepository
from typing_extensions import AsyncGenerator
from dto.message_chunk import StreamChunk, ChunkType


class RagAgent(AgentRepository):
    def __init__(self, workflow):
        self.workflow = workflow

    async def stream(self, msg: str) -> AsyncGenerator[StreamChunk, None]:
        try:
            inputs = {"messages": [HumanMessage(content=msg)]}

            async for chunk in self.workflow.astream(
                inputs,
                stream_mode="messages",
                version="v2",
            ):
                if chunk.get("type") != "messages":
                    continue

                msg_chunk, metadata = chunk["data"]
                node_name = metadata.get("langgraph_node")

                if hasattr(msg_chunk, "content") and msg_chunk.content:
                    yield {
                        "type": ChunkType.TOKEN,
                        "node": node_name,
                        "content": msg_chunk.content,
                        "end": False,
                    }

                if hasattr(msg_chunk, "tool_calls") and msg_chunk.tool_calls:
                    tool_names = [
                        tc.get("name") for tc in msg_chunk.tool_calls if tc.get("name")
                    ]
                    yield {
                        "type": ChunkType.TOKEN,
                        "node": node_name,
                        "content": f"\n\n> *Calling tools: {', '.join(tool_names)}...*\n\n",
                        "end": False,
                    }

            yield {
                "type": ChunkType.TOKEN,
                "node": None,
                "content": "",
                "end": True,
            }

        except Exception as e:
            print(f"ERROR IN STREAM: {e}", flush=True)
            raise e
