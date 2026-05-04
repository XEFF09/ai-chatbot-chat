import asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings


class LiliangwengStore:
    def __init__(self, embeddings: Embeddings, collection: str, cfg):
        self.cfg = cfg
        self._embeddings = embeddings
        self._collection = collection
        self._vector_store = None

    async def build(self):
        try:
            self._vector_store = QdrantVectorStore.from_existing_collection(
                embedding=self._embeddings,
                collection_name=self._collection,
                url=f"http://{self.cfg.qdrant_db_host}:{self.cfg.qdrant_db_port}",
            )
        except Exception:
            self._vector_store = await self._initialize_data()

        return self._vector_store

    async def _initialize_data(self) -> QdrantVectorStore:
        urls = [
            "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
            "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
            "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
        ]

        docs = await asyncio.gather(
            *[asyncio.to_thread(WebBaseLoader(url).load) for url in urls]
        )

        docs_list = [item for sublist in docs for item in sublist]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100,
        )

        splits = splitter.split_documents(docs_list)

        return QdrantVectorStore.from_documents(
            documents=splits,
            embedding=self._embeddings,
            url=f"http://{self.cfg.qdrant_db_host}:{self.cfg.qdrant_db_port}",
            collection_name=self._collection,
        )
