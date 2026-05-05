import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class AppConfig(BaseModel):
    grpc_port: int = Field(default_factory=lambda: int(os.getenv("GRPC_PORT", "50051")))
    grpc_domain: str = Field(
        default_factory=lambda: os.getenv("GRPC_DOMAIN", "0.0.0.0")
    )
    hf_api_token: str = Field(
        default_factory=lambda: os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    )
    qdrant_db_port: int = Field(
        default_factory=lambda: int(os.getenv("QDRANT_DB_PORT", "6334"))
    )
