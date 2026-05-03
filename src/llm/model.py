from config.config import AIConfig

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

cfg = AIConfig()

llm = HuggingFaceEndpoint(
    model="zai-org/GLM-5.1",
    temperature=0.7,
    max_new_tokens=1000,
    huggingfacehub_api_token=cfg.hf_api_token,
    streaming=True,
)
model = ChatHuggingFace(llm=llm)
