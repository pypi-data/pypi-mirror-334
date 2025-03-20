from transformers import AutoProcessor, SeamlessM4Tv2Model, SeamlessM4TModel
import torch
from typing import Union, List, Tuple
import pandas as pd
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator
from .utils import SEAMLESS_LANGS

class SeamlessTranslator(Translator):
    def __init__(self, model_name: str, detector: str) -> None:
        self.model_name = model_name
        self._check_model()
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        if 'v2' in self.model_name:
            self.model = SeamlessM4Tv2Model.from_pretrained(self.model_name)
        else:
            self.model = SeamlessM4TModel.from_pretrained(self.model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.detector = load_detector(detector)
        
    def _check_model(self):
        available_models = [
            'facebook/hf-seamless-m4t-large',
            'facebook/hf-seamless-m4t-medium',
            'facebook/seamless-m4t-v2-large'
        ]
        
        if self.model_name not in available_models:
            raise ValueError(f'{self.model_name} is not available. Please choose from {available_models}')
        
    def _get_language_code(self, text: str) -> Tuple[str, str]: # TODO: need to update the list of languages, beacuse seamless is not using en but eng, etc.
        language = self.detector.detect(text)
        return language, SEAMLESS_LANGS.get(language)
        
    def translate(self, text: Union[str, List[str]], dest: str) -> Union[str, List[str]]:
        is_list = isinstance(text, list)
        
        if not is_list:
            text = [text]
        
        translated = []
        
        for t in tqdm(text, desc='Translating', total=len(text)):
            lang, src_lang = self._get_language_code(t)
            
            if src_lang == dest:
                translated.append(t)
                continue
            
            text_inputs = self.processor(text=t, src_lang=src_lang, return_tensors="pt")
            
            output_tokens = self.model.generate(**text_inputs, tgt_lang=SEAMLESS_LANGS.get(dest), generate_speech=False)
            translated_text = self.processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
            translated.append(translated_text)
                
        if is_list:
            return translated
        else:
            return translated[0]
