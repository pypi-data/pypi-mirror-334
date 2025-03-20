from .detector import LanguageDetector
import requests

class LibreTranslateDetector(LanguageDetector):
    def __init__(self):
        self.url = "https://translate.flossboxin.org.in"
    
    def _preprocess(self, text: str) -> str:
        return text.replace('\n', ' ')

    def detect(self, text: str) -> str:
        text = self._preprocess(text)
        response = requests.post(f"{self.url}/detect", json={"q": text})
        
        output = response.json()
        return output[0]["language"]
        
    