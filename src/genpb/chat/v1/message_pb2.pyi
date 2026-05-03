import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChunkType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHUNK_TYPE_UNSPECIFIED: _ClassVar[ChunkType]
    TYPE_TOKEN: _ClassVar[ChunkType]
    TYPE_NODE_COMPLETE: _ClassVar[ChunkType]
CHUNK_TYPE_UNSPECIFIED: ChunkType
TYPE_TOKEN: ChunkType
TYPE_NODE_COMPLETE: ChunkType

class ChatMessageRequest(_message.Message):
    __slots__ = ("user_id", "message", "agent", "timestamp")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    message: str
    agent: str
    timestamp: int
    def __init__(self, user_id: _Optional[str] = ..., message: _Optional[str] = ..., agent: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class ErrorInfo(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ChatChunkResponse(_message.Message):
    __slots__ = ("token", "type", "node", "error", "is_final", "timestamp")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    token: str
    type: ChunkType
    node: str
    error: ErrorInfo
    is_final: bool
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, token: _Optional[str] = ..., type: _Optional[_Union[ChunkType, str]] = ..., node: _Optional[str] = ..., error: _Optional[_Union[ErrorInfo, _Mapping]] = ..., is_final: bool = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
