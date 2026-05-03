from typing import AsyncGenerator
from typing_extensions import AsyncIterable
import grpc

from genpb.chat.v1 import message_pb2, service_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from dto.message_chunk import ChunkType
from usecase.chat import ChatUsecase


class ChatHandler(service_pb2_grpc.ChatServiceServicer):
    def __init__(self, chat_service: ChatUsecase, ts: Timestamp):
        self.chat_service = chat_service
        self.ts = ts

        self.CHUNK_TYPE_MAP = {
            ChunkType.TOKEN: message_pb2.TYPE_TOKEN,
            ChunkType.NODE_COMPLETE: message_pb2.TYPE_NODE_COMPLETE,
            None: message_pb2.CHUNK_TYPE_UNSPECIFIED,
        }

    async def ChatStream(
        self, request_iterator: AsyncIterable[message_pb2.ChatMessageRequest], context
    ) -> AsyncGenerator[message_pb2.ChatChunkResponse, None]:
        try:
            async for request in request_iterator:
                responses = self.chat_service.execute_agent(
                    request.message,
                    request.agent,
                )

                async for data in responses:
                    now = self.ts.GetCurrentTime()

                    yield message_pb2.ChatChunkResponse(
                        token=data.get("content", ""),
                        type=self.CHUNK_TYPE_MAP.get(
                            data.get("type"), message_pb2.CHUNK_TYPE_UNSPECIFIED
                        ),
                        node=data.get("node") or "",
                        is_final=data.get("end", False),
                        timestamp=now,
                    )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            yield self._build_error_response(grpc.StatusCode.INTERNAL, str(e))

    def _build_error_response(
        self, code: grpc.StatusCode, message: str
    ) -> message_pb2.ChatChunkResponse:
        now = self.ts.GetCurrentTime()
        return message_pb2.ChatChunkResponse(
            error=message_pb2.ErrorInfo(
                code=str(code.value[0]),
                message=message,
            ),
            is_final=True,
            timestamp=now,
        )
