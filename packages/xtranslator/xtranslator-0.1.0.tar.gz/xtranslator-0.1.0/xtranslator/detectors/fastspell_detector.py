from fastspell import FastSpell
from .detector import LanguageDetector

class FastSpellDetector(LanguageDetector):
    def __init__(self):
        self.fsobj = FastSpell.FastSpell("en", mode="cons")

    def detect(self, text: str) -> str:
        return self.fsobj.getlang(text)