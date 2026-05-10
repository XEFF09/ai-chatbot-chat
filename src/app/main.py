import asyncio
import grpc
import logging
import sys
from grpc_reflection.v1alpha import reflection

from boostrap.embedding.hf import HfEmbeddings
from boostrap.llm import HfLLMModel
from genpb.chat.v1 import service_pb2_grpc, service_pb2
from internal.adapter.agent.rag import RagAgent
from internal.adapter.store.qdrant.lilianweng import LilianwengStore
from internal.adapter.tools.lilianweng import LilianwengToolSet
from internal.adapter.transport.grpc.chat import ChatHandler
from internal.adapter.workflow.critical import CriticalWorkflow
from internal.adapter.workflow.lilianweng import LilianwengWorkflow
from repository.agent import AgentFactoryImpl
from usecase.chat import ChatService

from internal.adapter.agent.critical import CriticalAgent
from config.config import AppConfig

from google.protobuf.timestamp_pb2 import Timestamp


cfg = AppConfig()
logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


async def init_rag(agent_factory, generate_model, grade_model, embeddings):
    lilianweng_store = await LilianwengStore(
        embeddings=embeddings,
        url=f"http://qdrant:{cfg.qdrant_db_port}",
        logger=logger,
    ).build()
    lilianweng_tool_set = LilianwengToolSet(lilianweng_store)
    rag_workflow = LilianwengWorkflow(
        generate_model, grade_model, lilianweng_tool_set.get_tools()
    ).get_graph()

    rag_agent = RagAgent(rag_workflow)
    agent_factory.register("lilianweng", rag_agent)


async def main():
    server = grpc.aio.server()

    ts = Timestamp()

    generate_model = HfLLMModel(cfg, "deepseek-ai/DeepSeek-V4-Flash").build()
    grade_model = HfLLMModel(cfg, "zai-org/GLM-5.1").build()
    embeddings = HfEmbeddings(cfg).build()

    critical_workflow = CriticalWorkflow(generate_model).get_graph()
    critical_agent = CriticalAgent(critical_workflow)

    agent_factory = AgentFactoryImpl()
    agent_factory.register("critical", critical_agent)

    await init_rag(agent_factory, generate_model, grade_model, embeddings)

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
