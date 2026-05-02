from dotenv import load_dotenv

import grpc
from grpc_reflection.v1alpha import reflection

from genpb.chat.v1 import service_pb2_grpc, service_pb2
from internal.adapter.transport.grpc.chat import ChatHandler
from usecase.chat import ChatService

from internal.adapter.agent.general import GeneralAgent
from langgraph.pregel.remote import RemoteGraph
from internal.middleware.logging import ErrorLoggerInterceptor


load_dotenv()

LANGGRAPH_URL = "http://127.0.0.1:2024"
general_rg = RemoteGraph("general_agent", url=LANGGRAPH_URL)


async def main():
    try:
        interceptors = [ErrorLoggerInterceptor()]
        server = grpc.aio.server(interceptors=interceptors)

        agent_repo = GeneralAgent(general_rg)
        chat_service = ChatService(agent_repo)
        chat_handler = ChatHandler(chat_service)
        service_pb2_grpc.add_ChatServiceServicer_to_server(chat_handler, server)

        SERVICE_NAMES = (
            service_pb2.DESCRIPTOR.services_by_name["ChatService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port("0.0.0.0:50051")
        await server.start()
        await server.wait_for_termination()

    except Exception as e:
        print(f"Error starting gRPC server: {e}")


if __name__ == "__main__":
    import asyncio

    print("Starting gRPC server on port 50051...")
    asyncio.run(main())
    print("gRPC server stopped.")
