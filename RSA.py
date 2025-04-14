import PrimeStuff as PS


class RSA:
    def __init__(self):
        self.p = PS.PrimeStuff.primeGen()
        self.q = PS.PrimeStuff.primeGen()
        self.e = PS.PrimeStuff.primeRelGen(self.phi())
        self.public_key = self.public_key_gen()
        self.private_key = self.private_key_gen()

    def phi(self):
        return (self.p - 1) * (self.q - 1)

    def public_key_gen(self):
        n = self.p * self.q
        public_key = [self.e, n]
        return public_key

    def private_key_gen(self):
        n = self.p * self.q
        d = PS.PrimeStuff.modInverse(self.e, self.phi())
        private_key = [d, n]
        return private_key

    def RSAEncrypt(self, msg, public_key):
        encrypted = msg ** public_key[0] % public_key[1]
        return encrypted

    def RSADecrypt(self, encrypted, private_key):
        decrypted = encrypted ** private_key[0] % private_key[1]
        return decrypted
