from repository.agent import AgentRepository
from typing_extensions import AsyncGenerator
from dto.message_chunk import StreamChunk, ChunkType


class CriticalAgent(AgentRepository):
    def __init__(self, rg):
        self.rg = rg

    async def receive(self, msg: str) -> AsyncGenerator[StreamChunk, None]:
        try:
            inputs = {"reqMessage": msg}
            async for chunk in self.rg.astream(
                inputs,
                stream_mode=["messages", "updates"],
                version="v2",
            ):
                if chunk.get("type") == "messages":
                    messge_chunk = chunk["data"][0]
                    content = messge_chunk.content

                    if content:
                        yield {
                            "type": ChunkType.TOKEN,
                            "node": None,
                            "content": content,
                            "end": False,
                        }

                elif chunk.get("type") == "updates":
                    for node_name, state in chunk["data"].items():
                        update_content = state.get("draft") or state.get("review")

                        if update_content:
                            yield {
                                "type": ChunkType.NODE_COMPLETE,
                                "node": node_name,
                                "content": update_content,
                                "end": False,
                            }

            yield {
                "type": None,
                "node": None,
                "content": "",
                "end": True,
            }
        except Exception as e:
            raise e
