from config.config import AIConfig

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.agents import create_agent

cfg = AIConfig()

llm = HuggingFaceEndpoint(
    model="zai-org/GLM-5.1",
    temperature=0.7,
    max_new_tokens=1000,
    huggingfacehub_api_token=cfg.hf_api_token,
)
model = ChatHuggingFace(llm=llm)

general_agent = create_agent(
    model=model, tools=[], system_prompt="You are a helpful assistant."
)
