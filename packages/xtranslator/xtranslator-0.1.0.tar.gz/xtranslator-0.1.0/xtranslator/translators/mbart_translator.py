from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, pipeline
import torch
from typing import Union, List, Tuple
import pandas as pd
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator
from .utils import MBART_LANGS

class MBARTTranslator(Translator):
    def __init__(
            self,
            model_name: str = 'facebook/mbart-large-50-many-to-many-mmt', 
            detector: str = None
        ) -> None:
        
        self.model_name = model_name
        self._check_model()
        self.tokenizer = MBart50TokenizerFast.from_pretrained(self.model_name)
        self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.detector = load_detector(detector)
        
    def _check_model(self):
        available_models = [
            'facebook/mbart-large-50-many-to-many-mmt',
        ]
        
        if self.model_name not in available_models:
            raise ValueError(f'{self.model_name} is not available. Please choose from {available_models}')
        
    def _get_language_code(self, text: str) -> Tuple[str, str]:
        language = self.detector.detect(text)
        return language, MBART_LANGS.get(language)
        
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
                tgt_lang=MBART_LANGS.get(dest)
            )
            
            result = trans_pipeline(t, src_lang=src_lang, tgt_lang=MBART_LANGS.get(dest))
            translation = [r['translation_text'] for r in result]
            translated_text = ' '.join(translation)
            translated.append(translated_text)
                
        if is_list:
            return translated
        else:
            return translated[0]
