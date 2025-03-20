# create abstract class for language detector

class LanguageDetector:
    
    def detect(self, text: str) -> str:
        raise NotImplementedError
    
    def detect_langs(self, text: str) -> dict:
        raise NotImplementedError
