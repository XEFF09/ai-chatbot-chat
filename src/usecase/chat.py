from typing import AsyncGenerator, Generator
from typing_extensions import Protocol
from repository.agent import AgentRepository


class ChatUsecase(Protocol):
    def execute_echo(self, message: str) -> Generator[str, None, None]: ...
    def execute_agent(self, message: str) -> AsyncGenerator[str, None]: ...


class ChatService(ChatUsecase):
    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo

    async def execute_agent(self, message: str) -> AsyncGenerator[str, None]:
        async for token in self.agent_repo.receive(message):
            yield token

    def execute_echo(self, message: str) -> Generator[str, None, None]:
        yield f"Echo: {message}"
