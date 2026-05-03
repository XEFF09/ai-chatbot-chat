import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessageRequest(_message.Message):
    __slots__ = ("user_id", "message", "timestamp")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    message: str
    timestamp: int
    def __init__(self, user_id: _Optional[str] = ..., message: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class ChatChunkResponse(_message.Message):
    __slots__ = ("delta", "is_final", "timestamp")
    DELTA_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    delta: str
    is_final: bool
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, delta: _Optional[str] = ..., is_final: bool = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
