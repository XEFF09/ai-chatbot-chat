import grpc
from grpc_reflection.v1alpha import reflection

from genpb.chat.v1 import service_pb2_grpc, service_pb2
from internal.adapter.transport.grpc.chat import ChatHandler
from repository.agent import AgentFactoryImpl
from usecase.chat import ChatService

from internal.adapter.agent.general import GeneralAgent
from langgraph.pregel.remote import RemoteGraph
from internal.middleware.logging import ErrorLoggerInterceptor
import logging
import sys

from config.config import AppConfig

cfg = AppConfig()

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


async def main():
    try:
        general_rg = RemoteGraph("general_agent", url=cfg.langgraph_url)
        general_agent_repo = GeneralAgent(general_rg)

        agent_factory = AgentFactoryImpl()
        agent_factory.register("general_agent", general_agent_repo)

        interceptors = [ErrorLoggerInterceptor(logger)]
        server = grpc.aio.server(interceptors=interceptors)

        chat_service = ChatService(agent_factory)
        chat_handler = ChatHandler(chat_service)
        service_pb2_grpc.add_ChatServiceServicer_to_server(chat_handler, server)

        SERVICE_NAMES = (
            service_pb2.DESCRIPTOR.services_by_name["ChatService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port(f"{cfg.grpc_domain}:{cfg.grpc_port}")
        await server.start()
        await server.wait_for_termination()

    except Exception as e:
        logger.info(f"Error starting gRPC server: {e}")


if __name__ == "__main__":
    import asyncio

    logger.info(f"Starting gRPC server on {cfg.grpc_domain}:{cfg.grpc_port}...")

    asyncio.run(main())
