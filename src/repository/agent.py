from typing_extensions import Protocol, AsyncGenerator
from typing import Dict


class AgentRepository(Protocol):
    async def receive(self, msg: str) -> AsyncGenerator: ...


class AgentFactory(Protocol):
    def register(self, agent_name: str, agent: AgentRepository): ...
    def get_agent(self, agent_name: str) -> AgentRepository: ...


class AgentFactoryImpl(AgentFactory):
    def __init__(self):
        self._agents: Dict[str, AgentRepository] = {}

    def register(self, agent_name: str, agent: AgentRepository):
        self._agents[agent_name] = agent

    def get_agent(self, agent_name: str) -> AgentRepository:
        agent = self._agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        return agent
