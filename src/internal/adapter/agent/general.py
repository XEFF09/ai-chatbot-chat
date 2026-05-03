from repository.agent import AgentRepository
from typing_extensions import AsyncGenerator, TypedDict


class StreamChunk(TypedDict):
    content: str
    end: bool


class GeneralAgent(AgentRepository):
    def __init__(self, rg):
        self.rg = rg

    async def receive(self, msg: str) -> AsyncGenerator[StreamChunk, None]:
        try:
            async for chunk in self.rg.astream(
                {"messages": [{"role": "user", "content": msg}]},
                stream_mode="messages",
                version="v2",
            ):
                if chunk.get("type") == "messages":
                    message_chunk = chunk["data"][0]
                    content = message_chunk.get("content", "")

                    if content:
                        yield {"content": content, "end": False}

            yield {"content": "", "end": True}

        except Exception as e:
            raise e
