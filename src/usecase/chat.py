from typing import AsyncGenerator, Generator
from typing_extensions import Protocol
from repository.agent import AgentFactory


class ChatUsecase(Protocol):
    def execute_echo(self, message: str) -> Generator: ...
    def execute_agent(self, message: str) -> AsyncGenerator: ...


class ChatService(ChatUsecase):
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    async def execute_agent(self, message: str) -> AsyncGenerator:
        try:
            agent_repo = self.agent_factory.get_agent("general_agent")
            async for data in agent_repo.receive(message):
                yield data
        except Exception as e:
            raise e

    def execute_echo(self, message: str) -> Generator:
        yield f"Echo: {message}"
