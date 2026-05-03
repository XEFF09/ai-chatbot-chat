import asyncio
import grpc
import logging
import sys
from grpc_reflection.v1alpha import reflection

from genpb.chat.v1 import service_pb2_grpc, service_pb2
from internal.adapter.transport.grpc.chat import ChatHandler
from repository.agent import AgentFactoryImpl
from usecase.chat import ChatService

from internal.adapter.agent.critical import CriticalAgent
from langgraph.pregel.remote import RemoteGraph
from config.config import AppConfig

from google.protobuf.timestamp_pb2 import Timestamp

cfg = AppConfig()
logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


async def main():
    ts = Timestamp()

    critical_rg = RemoteGraph("critical_graph", url=cfg.langgraph_url)
    critical_agent_repo = CriticalAgent(critical_rg)

    agent_factory = AgentFactoryImpl()
    agent_factory.register("critical", critical_agent_repo)

    server = grpc.aio.server()

    chat_service = ChatService(agent_factory)
    chat_handler = ChatHandler(chat_service, ts)
    service_pb2_grpc.add_ChatServiceServicer_to_server(chat_handler, server)

    SERVICE_NAMES = (
        service_pb2.DESCRIPTOR.services_by_name["ChatService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f"{cfg.grpc_domain}:{cfg.grpc_port}")
    await server.start()
    logger.info(f"gRPC server active on {cfg.grpc_domain}:{cfg.grpc_port}")

    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        logger.info("Shutdown signal received. Closing streams...")
        await server.stop(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.error(f"Server crashed: {e}")
