from typing import Union, List
import pandas as pd
from tqdm import tqdm
import requests
from .translator import Translator

class LibreTranslateTranslator(Translator):
    def __init__(self, model_name: str, detector: str = None) -> None:
        self.model_name = model_name
        self.url = "https://translate.flossboxin.org.in"
        self.detector = None
        
    def translate(self, text: Union[str, List[str]], dest: str) -> Union[str, List[str]]:
        is_list = isinstance(text, list)
        
        if not is_list:
            text = [text]

        translated = []
        
        for t in tqdm(text, desc='Translating', total=len(text)):
            response = requests.post(f"{self.url}/translate", json={
                "q": t,
                "source": "auto",
                "target": dest
            })
            translated_text = response.json()["translatedText"]
            translated.append(translated_text)
        
        if is_list:
            return translated
        else:
            return translated[0]
