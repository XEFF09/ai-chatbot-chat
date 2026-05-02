from typing_extensions import Protocol, AsyncGenerator


class AgentRepository(Protocol):
    async def receive(self, msg: str) -> AsyncGenerator: ...
