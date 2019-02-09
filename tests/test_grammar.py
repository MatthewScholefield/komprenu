from komprenu.grammar import Grammar


class TestGrammar:
    def setup(self):
        self.grammar = Grammar(4, 4)
        assert len(self.grammar.word_bits) > 0

    def test_ingest(self):
        assert set(self.grammar.ingest(1)) == {0, 1, 2, 3}
