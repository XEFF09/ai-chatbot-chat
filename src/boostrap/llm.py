from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
)


class HfLLMModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self._model = None

    def build(self):
        llm = HuggingFaceEndpoint(
            model="zai-org/GLM-5.1",
            temperature=0.7,
            max_new_tokens=1000,
            huggingfacehub_api_token=self.cfg.hf_api_token,
            streaming=True,
        )
        self._model = ChatHuggingFace(llm=llm)
        return self._model
