from ftlangdetect import detect
from .detector import LanguageDetector

class FastTextDetector(LanguageDetector):
    def __init__(self):
        pass
    
    def _preprocess(self, text: str) -> str:
        return text.replace('\n', ' ')

    def detect(self, text: str) -> str:
        text = self._preprocess(text)
        result = detect(text=text, low_memory=False)
        return result['lang']
    