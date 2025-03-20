import unittest

from xtranslator.detectors import simplemma_detector, langid_detector, fasttext_detector, google_detector, langdetect_detector, lingua_detector, stanza_detector, glotlid, libre_detector


class TestDetectors(unittest.TestCase):
    # def test_cld3_detector(self):
    #     detector = cld3_detector.CLD3Detector()
    #     self.assertEqual(detector.detect('Hello, world!'), 'en')

    def test_langid_detector(self):
        detector = langid_detector.LangidDetector()
        self.assertEqual(detector.detect('Ahoj ako sa máš'), 'sk')

    def test_simplemma_detector(self):
        detector = simplemma_detector.SimpleMMADetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')

    # def test_fastspell_detector(self):
    #     detector = fastspell_detector.FastSpellDetector()
    #     self.assertEqual(detector.detect('Hello, world!'), 'en')

    def test_fasttext_detector(self):
        detector = fasttext_detector.FastTextDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')

    def test_google_detector(self):
        detector = google_detector.GoogleDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')

    def test_langdetect_detector(self):
        detector = langdetect_detector.LangdetectDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')

    def test_lingua_detector(self):
        detector = lingua_detector.LinguaDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')

    def test_stanza_detector(self):
        detector = stanza_detector.StanzaDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')
        
    def test_glotlid_detector(self):
        detector = glotlid.GlotLIDDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')
        
    def test_libre_detector(self):
        detector = libre_detector.LibreTranslateDetector()
        self.assertEqual(detector.detect('Hello, world!'), 'en')
        
if __name__ == '__main__':
    unittest.main()