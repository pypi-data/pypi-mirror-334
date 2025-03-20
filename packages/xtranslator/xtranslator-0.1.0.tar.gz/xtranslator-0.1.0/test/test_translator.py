import unittest

from xtranslator.translators import translate

class TestTranslators(unittest.TestCase):
    def test_amazon_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'amazon'
        model_name = 'amazon'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Ahoj, svet!')
    
    def test_google_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'google'
        model_name = 'google'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Ahoj svet!')
        
    def test_deepl_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'deepl'
        model_name = 'deepl'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Ahoj, svet!')
        
    def test_m2m100_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'm2m100'
        model_name = 'facebook/m2m100_418M'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Dobrý deň svet!')
        
    def test_madlad_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'madlad'
        model_name = 'google/madlad400-3b-mt'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Ahoj, svet!')
        
    def test_mbart_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'mbart'
        model_name = 'facebook/mbart-large-50-many-to-many-mmt'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'sk, world!')
        
    def test_nllb_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'nllb'
        model_name = 'facebook/nllb-200-distilled-600M'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Ahoj, svet!')
        
    def test_seamless_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'seamless'
        model_name = 'facebook/hf-seamless-m4t-medium'
        detector = 'fasttext'
        
        self.assertEqual(translate(text, dest, translator, model_name, detector), 'Dobrý deň, svet!')
        
    def test_libre_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'libre'
        model_name = 'libre'
        detector = 'fasttext'
        
        result = translate(text, dest, translator, model_name, detector)
        self.assertEqual(result, 'Ahoj, svet!')
        
    def test_argostranslate_translator(self):
        text = 'Hello, world!'
        dest = 'sk'
        translator = 'argostranslate'
        model_name = 'argostranslate'
        detector = 'fasttext'
        
        result = translate(text, dest, translator, model_name, detector)
        print(result)
        self.assertEqual(result, 'Ahoj, svet!')
        
if __name__ == '__main__':
    unittest.main()
        