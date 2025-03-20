import deepl
import os
from typing import Union, List
import pandas as pd
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator

class DeepLTranslator(Translator):
    def __init__(self, model_name: str, detector: str) -> None:
        self.model_name = model_name
        auth_key = os.getenv('DEEPL_AUTH_KEY')
        
        self.client = deepl.Translator(auth_key)
        self.detector = load_detector(detector)
        
    def _get_language_code(self, text: str) -> str:
        language = self.detector.detect(text)
        return language
        
    def translate(self, text: Union[str, List[str]], dest: str) -> Union[str, List[str]]:
        is_list = isinstance(text, list)
        
        if not is_list:
            text = [text]
        
        translated = []
    
        for t in tqdm(text, desc='Translating', total=len(text)):
            src_lang = self._get_language_code(t)
            
            if src_lang == dest:
                translated.append(t)
                continue
            
            response = self.client.translate_text(
                t,
                source_lang=src_lang,
                target_lang=dest.upper()
            )
            
            translated_text = response.text
            translated.append(translated_text)
            
        if is_list:
            return translated
        else:
            return translated[0]
