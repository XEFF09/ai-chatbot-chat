from repository.agent import AgentRepository
from typing_extensions import AsyncGenerator


class GeneralAgent(AgentRepository):
    def __init__(self, rg):
        self.rg = rg

    async def receive(self, msg: str) -> AsyncGenerator[str, None]:
        try:
            async for event in self.rg.astream(
                {"messages": [{"role": "user", "content": msg}]},
                stream_mode="updates",
            ):
                for node_name, node_data in event.items():
                    if "messages" in node_data:
                        last_message = node_data["messages"][-1]

                        if isinstance(last_message, dict):
                            content = last_message.get("content")
                            msg_type = last_message.get("type")
                        else:
                            content = getattr(last_message, "content", "")
                            msg_type = getattr(last_message, "type", "")

                        if msg_type == "ai" and content:
                            yield content
        except Exception as e:
            print(f"Error in GeneralAgent: {e}")
            raise e
