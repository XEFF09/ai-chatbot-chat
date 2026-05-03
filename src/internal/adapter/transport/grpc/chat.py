from genpb.chat.v1 import message_pb2, service_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import time
from usecase.chat import ChatUsecase
from typing_extensions import AsyncIterable


class ChatHandler(service_pb2_grpc.ChatServiceServicer):
    def __init__(self, chat_service: ChatUsecase):
        self.chat_service = chat_service

    async def ChatStream(
        self, request_iterator: AsyncIterable[message_pb2.ChatMessageRequest], context
    ):
        try:
            async for request in request_iterator:
                responses = self.chat_service.execute_agent(request.message)

                async for data in responses:
                    now = time.time()
                    ts = Timestamp()
                    ts.seconds = int(now)
                    ts.nanos = int((now - ts.seconds) * 10**9)

                    yield message_pb2.ChatChunkResponse(
                        delta=data.get("content", ""),
                        is_final=data.get("end", False),
                        timestamp=ts,
                    )
        except Exception as e:
            yield message_pb2.ChatChunkResponse(
                delta=f"Error: {str(e)}",
                is_final=True,
            )
            raise e
