import re
from typing import List

TOKEN_RE = re.compile(r"\b[А-Яа-яЁёA-Za-z0-9']+\b")

def tokenize(text: str) -> List[str]:
    if not isinstance(text, str):
        text = str(text)
    return TOKEN_RE.findall(text)