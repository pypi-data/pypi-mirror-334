from googletrans import Translator
from .detector import LanguageDetector


class GoogleDetector(LanguageDetector):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
    
    def detect(self, text: str) -> str:
        import asyncio
        output = asyncio.run(self.translator.detect(text))
        return output.lang
