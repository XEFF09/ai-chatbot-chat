from typing import AsyncGenerator, Generator
from typing_extensions import Protocol
from repository.agent import AgentRepository


class ChatUsecase(Protocol):
    def execute_echo(self, message: str) -> Generator: ...
    def execute_agent(self, message: str) -> AsyncGenerator: ...


class ChatService(ChatUsecase):
    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo

    async def execute_agent(self, message: str) -> AsyncGenerator:
        async for data in self.agent_repo.receive(message):
            yield data

    def execute_echo(self, message: str) -> Generator:
        yield f"Echo: {message}"
