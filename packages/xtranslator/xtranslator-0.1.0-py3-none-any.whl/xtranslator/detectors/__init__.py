# import xtranslator.detectors.cld3_detector as cld3_detector
# import xtranslator.detectors.fastspell_detector as fastspell_detector
import xtranslator.detectors.fasttext_detector as fasttext_detector
import xtranslator.detectors.google_detector as google_detector
import xtranslator.detectors.langdetect_detector as langdetect_detector
import xtranslator.detectors.langid_detector as langid_detector
import xtranslator.detectors.lingua_detector as lingua_detector
import xtranslator.detectors.simplemma_detector as simplemma_detector
import xtranslator.detectors.stanza_detector as stanza_detector
import xtranslator.detectors.libre_translate as libre_detector

def detect(text: str, detector: str) -> str:
    detector = load_detector(detector)
    
    return detector.detect(text)


def load_detector(provider: str):
    # if provider == 'cld3':
    #     return cld3_detector.CLD3Detector()
    # if provider == 'fastspell':
    #     return fastspell_detector.FastSpellDetector()
    if provider == 'fasttext':
        return fasttext_detector.FastTextDetector()
    elif provider == 'google':
        return google_detector.GoogleDetector()
    elif provider == 'langdetect':
        return langdetect_detector.LangdetectDetector()
    elif provider == 'langid':
        return langid_detector.LangidDetector()
    elif provider == 'lingua':
        return lingua_detector.LinguaDetector()
    elif provider == 'simplemma':
        return simplemma_detector.SimpleMMADetector()
    elif provider == 'stanza':
        return stanza_detector.StanzaDetector()
    elif provider == 'libre':
        return libre_detector.LibreTranslateDetector()
    else:
        raise ValueError(f'{provider} is not available. Please choose from facebook, google, or microsoft')