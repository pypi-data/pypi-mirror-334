import fasttext
from huggingface_hub import hf_hub_download
from .detector import LanguageDetector
from .utils import GLOTLID_MAPPING

class GlotLIDDetector(LanguageDetector):
    def __init__(self):
        self.model_path = hf_hub_download(repo_id="cis-lmu/glotlid", filename="model.bin", cache_dir=None)
        self.model = fasttext.load_model(self.model_path)
    
    def _preprocess(self, text: str) -> str:
        return text.replace('\n', ' ')
    
    def _get_lang(self, lang: str) -> str:
        return GLOTLID_MAPPING.get(lang, lang)

    def detect(self, text: str) -> str:
        text = self._preprocess(text)
        langs, scores = self.model.predict(text, k=3)
        lang_pairs = {lang.split("__")[2]: score.item() for lang, score in zip(langs, scores)}
        best_lang_pair = max(lang_pairs.items(), key=lambda x: x[1])
        lang = self._get_lang(best_lang_pair[0].split("_")[0])
        return lang
    