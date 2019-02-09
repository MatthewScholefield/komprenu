import random
from bitarray import bitarray


class WordBits:
    MUT_ACT = 0.001
    MUT_AND = 0.001
    MUT_XOR = 0.1
    MUT_OR = 0.001

    def __init__(self, latent_len=0):
        self.activate_bits = bitarray(latent_len)
        self.activate_bits[::] = 0
        self.and_bits = bitarray(latent_len)
        self.xor_bits = bitarray(latent_len)
        self.or_bits = bitarray(latent_len)
        self.and_bits[::] = 1
        self.xor_bits[::] = 0
        self.or_bits[::] = 0

    def modify_state(self, state):
        state &= self.and_bits
        state ^= self.xor_bits
        state |= self.or_bits

        return state

    def is_activated(self, state):
        return self.activate_bits & state == self.activate_bits

    def mutate(self):
        for i in range(len(self.and_bits)):
            r = random.random()
            if r < self.MUT_ACT:
                self.activate_bits[i] ^= 1
            if r < self.MUT_AND:
                self.and_bits[i] ^= 1
            if r < self.MUT_XOR:
                self.xor_bits[i] ^= 1
            if r < self.MUT_OR:
                self.or_bits[i] ^= 1

    def serialize(self):
        return {
            'activate': self.activate_bits.tobytes().hex(),
            'and': self.and_bits.tobytes().hex(),
            'xor': self.xor_bits.tobytes().hex(),
            'or': self.or_bits.tobytes().hex()
        }

    def deserialize(self, data):
        self.activate_bits = bytearray.fromhex(data['activate'])
        self.and_bits = bytearray.fromhex(data['and'])
        self.xor_bits = bytearray.fromhex(data['xor'])
        self.or_bits = bytearray.fromhex(data['or'])
