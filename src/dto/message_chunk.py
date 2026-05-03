from typing_extensions import AsyncGenerator, TypedDict, Optional
from enum import Enum


class ChunkType(Enum):
    TOKEN = "token"
    NODE_COMPLETE = "node_complete"


class StreamChunk(TypedDict):
    type: Optional[ChunkType]
    node: Optional[str]
    content: str
    end: bool
