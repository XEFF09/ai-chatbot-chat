import asyncio
from logging import Logger
from langchain_community.document_loaders import WebBaseLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


class LilianwengStore:
    def __init__(self, embeddings: Embeddings, url: str, logger: Logger):
        self._embeddings = embeddings
        self._vector_store = None
        self._collection = "lilianweng-collection"
        self._url = url
        self._logger = logger

    async def build(self):
        try:
            self._vector_store = QdrantVectorStore.from_existing_collection(
                embedding=self._embeddings,
                collection_name=self._collection,
                url=self._url,
            )
        except Exception:
            self._logger.info(
                " ---------- Collection not found. Initializing new collection and ingesting data ---------- "
            )
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
        cleaned_docs = await asyncio.to_thread(self._clean_documents, docs_list)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100,
        )

        splits = splitter.split_documents(cleaned_docs)

        return await asyncio.to_thread(
            QdrantVectorStore.from_documents,
            documents=splits,
            embedding=self._embeddings,
            url=self._url,
            collection_name=self._collection,
        )

    def _clean_documents(self, documents: list[Document]) -> list[Document]:
        """Clean HTML content from documents using BeautifulSoup."""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            self._logger.warning("BeautifulSoup not installed, skipping HTML cleaning")
            return documents

        cleaned_docs = []
        for doc in documents:
            try:
                soup = BeautifulSoup(doc.page_content, "html.parser")

                for script in soup(["script", "style", "nav", "footer"]):
                    script.decompose()

                text = soup.get_text(separator="\n", strip=True)

                lines = [line.strip() for line in text.split("\n")]
                text = "\n".join(line for line in lines if line)

                cleaned_doc = Document(page_content=text, metadata=doc.metadata)
                cleaned_docs.append(cleaned_doc)
            except Exception as e:
                self._logger.warning(f"Error cleaning document: {e}, keeping original")
                cleaned_docs.append(doc)

        return cleaned_docs
