import random
from tqdm import tqdm
from copy import deepcopy

import json
from typing import List, Iterable

from komprenu.grammar import Grammar
from komprenu.util import tokenize
from komprenu.vocab import Vocab


class Model:
    def __init__(self, vocab_len, latent_len=10):
        self.grammar = Grammar(vocab_len, latent_len)
        self.vocab = Vocab()

    def train(self, sentence_lines: Iterable[str], vocab_len=100, iterations=1000, lines=10):
        print('Tokenizing...')
        sentence_tokens = list(tqdm(tokenize(i) for i in sentence_lines))

        print('Collecting all words...')
        all_words = (j for i in sentence_tokens for j in i)

        print('Loading vocab...')
        self.vocab.set_vocab(all_words, vocab_len)

        all_sent_indices = [self.vocab.encode(i) for i in sentence_tokens]

        best_grammar = self.grammar
        best_score = float('-inf')

        for iter_num in range(iterations):
            test_grammar = deepcopy(best_grammar)
            test_grammar.mutate()
            test_score = 0
            for sent_indices in all_sent_indices[:lines]:
                test_grammar.reset()
                score = 0
                for ind, next_ind in zip(sent_indices, sent_indices[1:]):
                    prev_state = test_grammar.state.copy()
                    possible_words = test_grammar.ingest(ind)
                    diff = (prev_state ^ test_grammar.state)
                    has_word = next_ind in possible_words
                    score -= len(possible_words) - has_word
                    score += has_word + sum(diff)
                test_score += score
            print('\rScore:', test_score, end='')
            if test_score > best_score:
                best_score = test_score
                best_grammar = test_grammar
        print('\nBest score:', best_score)
        self.grammar = best_grammar

    def walk(self, n):
        self.grammar.reset()
        prev_word = self.vocab['this']
        for i in range(n):
            next_words = self.grammar.ingest(prev_word)
            print(self.vocab.decode(next_words))
            print(self.grammar.state.tobytes().hex())
            next_word = random.choice(next_words)
            yield self.vocab[next_word]
            prev_word = next_word

    def load(self, filename):
        with open(filename) as f:
            data = json.load(f)
        self.grammar.deserialize(data['grammar'])
        self.vocab.deserialize(data['vocab'])

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump({
                'grammar': self.grammar.serialize(),
                'vocab': self.vocab.serialize()
            }, f)
