from lingua import LanguageDetectorBuilder
from .detector import LanguageDetector

class LinguaDetector(LanguageDetector):
    def __init__(self):
        self.detector = LanguageDetectorBuilder.from_all_languages().build()

    def detect(self, text: str) -> str:
        return self.detector.detect_language_of(text).iso_code_639_1.name.lower()
    
    def _convert(self, confidence_values: dict) -> dict:
        return {confidence.language.iso_code_639_1.name.lower(): confidence.value for confidence in confidence_values}

    def detecet_langs(self, text: str) -> dict:
        confidence_values = self.detector.compute_language_confidence_values("languages are awesome")
        return self._convert(confidence_values)
