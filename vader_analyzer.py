from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from deep_translator import GoogleTranslator
from typing import Dict

analyzer = SentimentIntensityAnalyzer()

def _translate_to_en(text: str) -> str:
    try:
        lang = detect(text)
    except Exception:
        lang = 'auto'
    if lang != 'en':
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except Exception:
            return text
    return text

def analyze_vader(text: str, translate: bool = True) -> Dict[str, float]:
    safe_text = _translate_to_en(text) if translate else text
    scores = analyzer.polarity_scores(safe_text)
    return scores