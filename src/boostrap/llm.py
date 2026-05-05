from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
)


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
