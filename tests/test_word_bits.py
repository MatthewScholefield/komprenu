from bitarray import bitarray

from komprenu.word_bits import WordBits


class TestWordBits:
    def setup(self):
        self.bits = WordBits(4)
        self.state = bitarray('0000')

    def test_is_activated(self):
        assert self.bits.is_activated(self.state)
        self.state[0] = 1
        assert self.bits.is_activated(self.state)
        self.bits.activate_bits[:2] = 1
        assert not self.bits.is_activated(self.state)
        self.state[1] = 1
        assert self.bits.is_activated(self.state)

    def test_mutate(self):
        WordBits.MUT_ACT = WordBits.MUT_OR = WordBits.MUT_AND = WordBits.MUT_XOR = 1.0
        self.bits.mutate()
        assert self.bits.activate_bits == bitarray('1111')
        assert self.bits.and_bits == bitarray('0000')
        assert self.bits.xor_bits == bitarray('1111')
        assert self.bits.or_bits == bitarray('1111')

    def test_ingest(self):
        assert self.bits.modify_state(bitarray('1111')) == bitarray('1111')
        self.bits.and_bits = bitarray('1100')
        assert self.bits.modify_state(bitarray('1101')) == bitarray('1100')
        self.bits.or_bits = bitarray('0010')
        assert self.bits.modify_state(bitarray('1100')) == bitarray('1110')
