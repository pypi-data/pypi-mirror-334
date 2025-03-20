from langdetect import detect, detect_langs
from .detector import LanguageDetector

class LangdetectDetector(LanguageDetector):
    def __init__(self):
        super().__init__()
        
    def _preprocess(self, text: str) -> str:
        return text.replace('\n', ' ')
        
    def detect(self, text: str) -> str:
        text = self._preprocess(text)
        return detect(text)
    
    def detect_langs(self, text: str) -> dict:
        text = self._preprocess(text)
        return detect_langs(text)
