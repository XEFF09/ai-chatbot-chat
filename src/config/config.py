import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class AppConfig(BaseModel):
    langgraph_url: str = Field(
        default_factory=lambda: os.getenv("LANGGRAPH_URL", "http://localhost:2024")
    )
    grpc_port: int = Field(default_factory=lambda: int(os.getenv("GRPC_PORT", "50051")))
    grpc_domain: str = Field(
        default_factory=lambda: os.getenv("GRPC_DOMAIN", "localhost")
    )
    reload: bool = Field(
        default_factory=lambda: os.getenv("DEBUG", "true").lower() == "true"
    )

    hf_api_token: str = Field(
        default_factory=lambda: os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    )
    langgraph_tracing: bool = Field(
        default_factory=lambda: os.getenv("LANGGRAPH_TRACING", "false").lower()
        == "true"
    )
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    qdrant_db_host: str = Field(
        default_factory=lambda: os.getenv("QDRANT_DB_HOST", "localhost")
    )
    qdrant_db_port: int = Field(
        default_factory=lambda: int(os.getenv("QDRANT_DB_PORT", "6334"))
    )
