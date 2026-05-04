from langchain.tools import BaseTool
from typing_extensions import Protocol


class ToolSet(Protocol):
    def get_tools(self) -> list[BaseTool]: ...
