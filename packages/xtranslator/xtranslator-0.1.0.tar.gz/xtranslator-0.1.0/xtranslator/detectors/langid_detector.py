import langid
from .detector import LanguageDetector

class LangidDetector(LanguageDetector):
    def __init__(self):
        super().__init__()
        
    def _preprocess(self, text: str) -> str:
        return text.replace('\n', ' ')
    
    def detect(self, text: str) -> str:
        text = self._preprocess(text)
        result = langid.classify(text)
        return result[0]