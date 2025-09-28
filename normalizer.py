from typing import List, Iterable
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import re

try:
    _ = stopwords.words('russian')
except Exception:
    import nltk as _n
    _n.download('stopwords')
    _n.download('wordnet')
    _n.download('omw-1.4')

DEFAULT_STOPWORDS = set(stopwords.words('russian')) if 'russian' in stopwords.fileids() else set(stopwords.words('english'))

RE_PUNCT = re.compile(r"[^\w\s'-]")

class Normalizer:
    def __init__(self,
                lowercase: bool = True,
                remove_punct: bool = True,
                stop_words: Iterable[str] = None,
                do_stemming: bool = False,
                language: str = 'russian',
                synonym_map: dict = None):
            self.lowercase = lowercase
            self.remove_punct = remove_punct
            self.stop_words = set(stop_words) if stop_words is not None else DEFAULT_STOPWORDS
            self.do_stemming = do_stemming
            self.language = language
            self.synonym_map = synonym_map or {}

            if do_stemming:
                try:
                    self.stemmer = SnowballStemmer(language)
                except Exception:
                    self.stemmer = None
            else:
                self.stemmer = None

            self.lemmatizer = WordNetLemmatizer()

    def normalize_token(self, token: str) -> str:
        t = token
        if self.lowercase:
            t = t.lower()
        if self.remove_punct:
            t = RE_PUNCT.sub('', t)
        if not t:
            return ''
        if t in self.synonym_map:
            t = self.synonym_map[t]
        if self.do_stemming and self.stemmer:
            t = self.stemmer.stem(t)
        else:
            try:
                t = self.lemmatizer.lemmatize(t)
            except Exception:
                pass
        if t in self.stop_words:
            return ''
        return t

    def normalize(self, tokens: Iterable[str]) -> List[str]:
        out = []
        for token in tokens:
            n = self.normalize_token(token)
            if n:
                out.append(n)
        return out