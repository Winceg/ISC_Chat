import PrimeStuff as PS
import crypto_logic as cl
import os

class DifHel():
    def __init__(self):
        self.p = PS.PrimeStuff.primeGen()
        self.g = PS.PrimeStuff.primeGen()

    def dh_half_key(self, key):
        # Generate a private key (random integer) and compute the public key
        private_key = int.from_bytes(os.urandom(16))  # Randomly generate a private key
        public_key = int(pow(self.g, private_key, self.p))  # Compute public key
        # public_key = pow(g, int.from_bytes(private_key, 'big'), p)  # Compute public key
        if key:
            #public = tuple(key.split(","))
            return cl.encodeMessage(key)
        else:
            #public = (self.p, self.g)
            #return public, public_key, private_key
            return cl.encodeMessage("1,1")

    def dh_encrypt(self, public_key_B):
        key = pow(public_key_B, self.dh_half_key[0], self.p)
        return cl.encodeMessage(1)