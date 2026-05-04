from langchain_huggingface import HuggingFaceEmbeddings


class HfEmbeddings:
    def __init__(self, cfg):
        self.cfg = cfg
        self._embeddings = None

    def build(self):
        self._embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            cache_folder="/root/.cache/huggingface",
            model_kwargs={"token": self.cfg.hf_api_token},
        )
        return self._embeddings
