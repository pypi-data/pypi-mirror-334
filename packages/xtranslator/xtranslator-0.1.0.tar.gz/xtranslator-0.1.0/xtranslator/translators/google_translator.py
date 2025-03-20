from googletrans import Translator as google_translator
import asyncio
from typing import Union, List
import pandas as pd
from tqdm import tqdm
from .translator import Translator

class GoogleTranslator(Translator):
    def __init__(self, model_name: str, detector: str = None) -> None:
        self.model_name = model_name
        
        self.translator = google_translator()
        self.detector = None
        
    def translate(self, text: Union[str, List[str]], dest: str) -> Union[str, List[str]]:
        is_list = isinstance(text, list)
        
        if not is_list:
            text = [text]

        translated = []
        
        for t in tqdm(text, desc='Translating', total=len(text)):
            output = asyncio.run(self.translator.translate(t, dest=dest))
            translated_text = output.text
            translated.append(translated_text)
        
        if is_list:
            return translated
        else:
            return translated[0]
