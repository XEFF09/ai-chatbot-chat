from genpb.chat.v1 import message_pb2, service_pb2_grpc
from usecase.chat import ChatUsecase


class ChatHandler(service_pb2_grpc.ChatServiceServicer):
    def __init__(self, chat_service: ChatUsecase):
        self.chat_service = chat_service

    async def ChatStream(self, request_iterator, context):
        async for request in request_iterator:
            responses = self.chat_service.execute_agent(request.message)

            async for data in responses:
                yield message_pb2.ChatChunkResponse(
                    content=data.get("content", ""),
                    done=data.get("end", False),
                )
