from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

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
    __slots__ = ("content", "done")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    content: str
    done: bool
    def __init__(self, content: _Optional[str] = ..., done: bool = ...) -> None: ...
