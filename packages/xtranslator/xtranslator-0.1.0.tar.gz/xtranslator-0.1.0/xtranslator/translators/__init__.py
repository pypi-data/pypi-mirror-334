import xtranslator.translators.amazon_translator as amazon_translator
import xtranslator.translators.google_translator as google_translator
import xtranslator.translators.deepl_translator as deepl_translator
import xtranslator.translators.m2m100_translator as m2m100_translator
import xtranslator.translators.madlad_translator as madlad_translator
import xtranslator.translators.mbart_translator as mbart_translator
import xtranslator.translators.nllb_translator as nllb_translator
import xtranslator.translators.seamless_translator as seamless_translator
import xtranslator.translators.libre_translate as libre_translator
import xtranslator.translators.argostranslate as argostranslate_translator
from typing import Union, List


def translate(text: Union[str, List[str]], dest: str, translator: str, model_name: str, detector: str) -> Union[str, List[str]]:
    translators = {
        'amazon': amazon_translator.AmazonTranslator,
        'google': google_translator.GoogleTranslator,
        'deepl': deepl_translator.DeepLTranslator,
        'm2m100': m2m100_translator.M2M100Translator,
        'madlad': madlad_translator.MADLADTranslator,
        'mbart': mbart_translator.MBARTTranslator,
        'nllb': nllb_translator.NLLBTranslator,
        'seamless': seamless_translator.SeamlessTranslator,
        'libre': libre_translator.LibreTranslateTranslator,
        'argostranslate': argostranslate_translator.ArgostranslateTranslator,
    }
    
    translator = translators[translator](model_name, detector)
    
    return translator.translate(text, dest)
        
def load_translator(translator: str, model_name: str, detector: str):
    translators = {
        'amazon': amazon_translator.AmazonTranslator,
        'google': google_translator.GoogleTranslator,
        'deepl': deepl_translator.DeepLTranslator,
        'm2m100': m2m100_translator.M2M100Translator,
        'madlad': madlad_translator.MADLADTranslator,
        'mbart': mbart_translator.MBARTTranslator,
        'nllb': nllb_translator.NLLBTranslator,
        'seamless': seamless_translator.SeamlessTranslator,
        'libre': libre_translator.LibreTranslateTranslator,
        'argostranslate': argostranslate_translator.ArgostranslateTranslator,
    }
    
    return translators[translator](model_name, detector)