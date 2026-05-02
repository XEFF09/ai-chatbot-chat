from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessage(_message.Message):
    __slots__ = ("user", "message", "timestamp")
    USER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    user: str
    message: str
    timestamp: int
    def __init__(self, user: _Optional[str] = ..., message: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...
