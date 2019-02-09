from typing import List
from bitarray import bitarray

from komprenu.word_bits import WordBits


class Grammar:
    def __init__(self, vocab_len=0, latent_len=10):
        self.word_bits = [WordBits(latent_len) for _ in range(vocab_len)]
        self.state = bitarray(latent_len)
        self.state[::] = 1

    def reset(self):
        self.state[::] = 1

    def ingest(self, word: int) -> List[int]:
        bits = self.word_bits[word]
        self.state = bits.modify_state(self.state)
        return [i for i, bits in enumerate(self.word_bits) if bits.is_activated(self.state)]

    def mutate(self):
        for bits in self.word_bits:
            bits.mutate()

    def serialize(self):
        return {
            'word_bits': [bits.serialize() for bits in self.word_bits],
            'latent_len': len(self.state)
        }

    def deserialize(self, data):
        self.word_bits = []
        for bits_data in data['word_bits']:
            self.word_bits.append(WordBits())
            self.word_bits[-1].deserialize(bits_data)
        self.state = bitarray(data['latent_len'])
        self.state[::] = 0
