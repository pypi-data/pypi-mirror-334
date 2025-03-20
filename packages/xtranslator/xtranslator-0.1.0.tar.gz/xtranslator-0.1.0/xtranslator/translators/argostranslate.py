from typing import Union, List
import argostranslate.package
import argostranslate.translate
from tqdm import tqdm
from xtranslator.detectors import load_detector
from .translator import Translator

class ArgostranslateTranslator(Translator):
    def __init__(self, model_name: str, detector: str = None) -> None:
        self.model_name = model_name
        self.detector = load_detector(detector)
        argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()
        
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
            package_to_install = next(
                filter(
                    lambda x: x.from_code == src_lang and x.to_code == dest, self.available_packages
                )
            )
            argostranslate.package.install_from_path(package_to_install.download())
            translated_text = argostranslate.translate.translate(t, src_lang, dest)
            translated.append(translated_text)
        
        if is_list:
            return translated
        else:
            return translated[0]
