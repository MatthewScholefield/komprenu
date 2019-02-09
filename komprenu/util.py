import re
from typing import List


def tokenize(sentence: str) -> List[str]:
    return sentence.lower().split()
