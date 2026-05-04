from typing import AsyncGenerator, Generator
from typing_extensions import Protocol
from repository.agent import AgentFactory

from dto.message_chunk import StreamChunk


class ChatUsecase(Protocol):
    def execute_echo(self, message: str) -> Generator: ...
    def execute_stream(
        self, message: str, agent: str
    ) -> AsyncGenerator[StreamChunk, None]: ...


class ChatService(ChatUsecase):
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    async def execute_stream(
        self, message: str, agent: str
    ) -> AsyncGenerator[StreamChunk, None]:
        try:
            agent_repo = self.agent_factory.get_agent(agent)
            async for data in agent_repo.stream(message):
                yield data
        except Exception as e:
            raise e

    def execute_echo(self, message: str) -> Generator:
        yield f"Echo: {message}"
