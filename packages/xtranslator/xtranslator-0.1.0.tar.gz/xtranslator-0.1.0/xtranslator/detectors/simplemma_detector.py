from simplemma import langdetect
from .detector import LanguageDetector

class SimpleMMADetector(LanguageDetector):
    def __init__(self):
        super().__init__()
        self.languages = (
            "ast", "bg", "ca", "cs", "cy", "da", "de", "el", "en", "enm", "es", "et", "fa", 
            "fi", "fr", "ga", "gd", "gl", "gv", "hbs", "hi", "hu", "hy", "id", "is", "it", 
            "ka", "la", "lb", "lt", "lv", "mk", "ms", "nb", "nl", "nn", "pl", "pt", "ro", 
            "ru", "se", "sk", "sl", "sq", "sv", "sw", "tl", "tr", "uk"
        )
    
    def _preprocess(self, text: str) -> str:
        return text.replace('\n', ' ')
    
    def detect(self, text: str) -> str:
        text = self._preprocess(text)
        languages = langdetect(text, lang=self.languages)
        languages = sorted(languages, key=lambda x: x[1], reverse=True)
        return languages[0][0]
                        
    def detect_langs(self, text: str) -> str:
        text = self._preprocess(text)
        return langdetect(text)
