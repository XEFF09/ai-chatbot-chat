# from langchain_community.document_loaders import WebBaseLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain.tools import tool
#
# from config.config import AppConfig
# from langchain_huggingface import HuggingFaceEmbeddings
#
# cfg = AppConfig()
#
# _vector_store = None
#
#
# async def get_retriever():
#     """Initializes the vector store only when needed."""
#     global _vector_store
#     if _vector_store is not None:
#         return _vector_store.as_retriever()
#
#     print("--- Initializing Vector Store (This may take a moment) ---", flush=True)
#
#     urls = [
#         "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
#         "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
#         "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
#     ]
#     docs = [WebBaseLoader(url).load() for url in urls]
#     docs_list = [item for sublist in docs for item in sublist]
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
#     dco_splits = text_splitter.split_documents(docs_list)
#
#     embedding_model = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-mpnet-base-v2",
#         cache_folder="/root/.cache/huggingface",
#         model_kwargs={"token": cfg.hf_api_token},
#     )
#
#     _vector_store = await InMemoryVectorStore.afrom_documents(
#         documents=dco_splits,
#         embedding=embedding_model,
#     )
#     return _vector_store.as_retriever()
#
#
# @tool
# async def retriever_tool(query: str) -> str:
#     """Search and return information about Lilian Weng blog posts."""
#     retriever = await get_retriever()
#     docs = await retriever.ainvoke(query)
#     return "\n\n".join([doc.page_content for doc in docs])
