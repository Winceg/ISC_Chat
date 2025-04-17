import PrimeStuff as PS
import crypto_logic as logic
import os


def dh_encrypt(B=0, a=0, p=0):
    key = pow(B, a, p)
    return key


class DifHel():
    def __init__(self, p=0, g=0):
        self.p = p if p != 0 else PS.PrimeStuff.primeGen()
        self.g = g if g != 0 else PS.PrimeStuff.primeRelGen(p)

    def dh_half_key(self, key):
        # Generate a private key (random integer) and compute the public key
        private_key = int.from_bytes(os.urandom(16))  # Randomly generate a private key
        public_key = int(pow(self.g, private_key, self.p))  # Compute public key
        # public_key = pow(g, int.from_bytes(private_key, 'big'), p)  # Compute public key
        if key == "":
            return logic.encodeMessage(f"{str(self.p)},{str(self.g)}")
        else:
            # public = tuple(key.split(","))
            return logic.encodeMessage(key)
