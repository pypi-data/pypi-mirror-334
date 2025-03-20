from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer, pipeline
import torch
from typing import Union, List, Tuple
import pandas as pd
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator
from .utils import M2M_LANGS

class M2M100Translator(Translator):
    def __init__(self, model_name: str, detector: str) -> None:
        self.model_name = model_name
        self._check_model()
        self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
        self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.detector = load_detector(detector)
        
    def _check_model(self):
        available_models = [
            'facebook/m2m100_418M',
            'facebook/m2m100_1.2B',
            'facebook/m2m100-12B-avg-10-ckpt',
            'facebook/m2m100-12B-avg-5-ckpt',
            'facebook/m2m100-12B-last-ckpt',
        ]
        
        if self.model_name not in available_models:
            raise ValueError(f'{self.model_name} is not available. Please choose from {available_models}')
            
    def _get_language_code(self, text: str) -> Tuple[str, str]:
        language = self.detector.detect(text)
        return language, M2M_LANGS.get(language)
        
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
            
            trans_pipeline = pipeline(
                'translation', 
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
                src_lang=src_lang,
                tgt_lang=M2M_LANGS.get(dest)
            )
            
            result = trans_pipeline(t)
            translation = [r['translation_text'] for r in result]
            translated_text = ' '.join(translation)
            translated.append(translated_text)
            
        if is_list:
            return translated
        else:
            return translated[0]
