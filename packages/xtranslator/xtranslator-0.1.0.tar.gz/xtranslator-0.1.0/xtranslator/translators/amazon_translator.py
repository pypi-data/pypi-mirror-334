import boto3
import os
from typing import Union, List
import pandas as pd
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator

class AmazonTranslator(Translator):
    def __init__(self, model_name: str, detector: str) -> None:
        self.model_name = model_name
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_REGION')
        
        self.client = boto3.client(
            'translate',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region,
        )
        self.detector = load_detector(detector)
        
    def _get_language_code(self, text):
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
                Text=t,
                SourceLanguageCode=src_lang,
                TargetLanguageCode=dest
            )
            
            translated_text = response['TranslatedText']
            translated.append(translated_text)
                
        if is_list:
            return translated
        else:
            return translated[0]
