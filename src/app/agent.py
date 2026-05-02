from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    model="zai-org/GLM-5.1",
    temperature=0.7,
    max_new_tokens=1000,
)
model = ChatHuggingFace(llm=llm)

general_agent = create_agent(
    model=model, tools=[], system_prompt="You are a helpful assistant."
)
