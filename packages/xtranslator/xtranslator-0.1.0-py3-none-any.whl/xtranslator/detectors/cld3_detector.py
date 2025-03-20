import gcld3
from .detector import LanguageDetector

class CLD3Detector(LanguageDetector):
    def __init__(self):
        self.lang_id = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)

    def detect(self, text):
        return self.lang_id.FindLanguage(text)
