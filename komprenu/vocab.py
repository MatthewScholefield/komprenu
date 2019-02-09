from collections import Counter
from itertools import chain

from tqdm import tqdm
from typing import List, Iterable

UNK = ':UNK-{}:'
UNK_CLASSES = 4


class Vocab(dict):
    UNK = UNK
    UNK_CLASSES = UNK_CLASSES

    TOKENS = [UNK.format(i) for i in range(UNK_CLASSES)]

    def __init__(self):
        super().__init__()
        self.words = list(self.TOKENS)
        self.unk_words = {}

    def set_vocab(self, all_words: Iterable, n=0):
        n = n or len(list(all_words))
        words_by_freq = list(tqdm(w for f, w in reversed(sorted((f, w) for w, f in Counter(
            all_words).items()))))

        cutoff = n - len(self.TOKENS)
        num_unk = max(0, len(words_by_freq) - cutoff)
        self.words = self.TOKENS + words_by_freq[:cutoff]
        self._update_mapping()
        self.unk_words = {word: self[self.UNK.format(int(((i ** 4) * (self.UNK_CLASSES - 1)) //
                                                max(1, num_unk - 1) ** 4))]
                          for i, word in enumerate(words_by_freq[cutoff:])}

    def __len__(self):
        return len(self.words)

    def _update_mapping(self):
        n = len(self.words)
        self.update(tqdm(chain(zip(self.words, range(n)), zip(range(n), self.words))))

    def encode(self, sentence: List[str]):
        return [self.get(i, self.unk_words.get(i, 0)) for i in sentence]

    def decode(self, indices: List[int]):
        return [self[i] for i in indices]

    def serialize(self):
        return {'words': self.words, 'unk_words': self.unk_words}

    def deserialize(self, data):
        self.words = data['words']
        self.unk_words = data['unk_words']
        self._update_mapping()
