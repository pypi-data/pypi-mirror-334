import stanza
from .detector import LanguageDetector

from stanza.models.common.doc import Document
from stanza.pipeline.core import Pipeline


class StanzaDetector(LanguageDetector):
    def __init__(self):
        stanza.download(lang="multilingual")
        self.nlp = Pipeline(lang="multilingual", processors="langid")
        print(self.nlp)

    def detect(self, text):
        doc = Document([], text=text)
        self.nlp(doc)
        return doc.lang