from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from typing import Union, List, Tuple
import pandas as pd
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator

class MADLADTranslator(Translator):
    def __init__(self, model_name: str, detector: str) -> None:
        self.model_name = model_name
        self._check_model()
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.detector = load_detector(detector)
         
    def _check_model(self):
        available_models = [
            'google/madlad400-3b-mt',
            'google/madlad400-7b-mt',
            'google/madlad400-10b-mt',
        ]
        
        if self.model_name not in available_models:
            raise ValueError(f'{self.model_name} is not available. Please choose from {available_models}')
        
    def _get_language_code(self, text: str) -> Tuple[str, str]:
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
            
            text = f'<2{src_lang}> {t}'
            
            input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)
            self.model.to(self.device)
            outputs = self.model.generate(input_ids=input_ids)
            
            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            translated.append(translated_text)
                
        if is_list:
            return translated
        else:
            return translated[0]
