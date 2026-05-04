from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
)
from langchain_openai import ChatOpenAI


class HfLLMModel:
    def __init__(self, cfg, model):
        self.cfg = cfg
        self._model = model
        self._model_instance = None

    def build(self):
        llm = HuggingFaceEndpoint(
            model=self._model,
            temperature=0.7,
            max_new_tokens=1000,
            huggingfacehub_api_token=self.cfg.hf_api_token,
            streaming=True,
        )
        self._model_instance = ChatHuggingFace(llm=llm)
        return self._model_instance


class OpenAILLMModel:
    def __init__(self, cfg, model="gpt-4-turbo"):
        self.cfg = cfg
        self._model = model
        self._model_instance = None

    def build(self):
        self._model_instance = ChatOpenAI(
            model=self._model,
            api_key=self.cfg.openai_api_key,
            temperature=0.7,
            max_completion_tokens=1000,
            streaming=True,
        )
        return self._model_instance
