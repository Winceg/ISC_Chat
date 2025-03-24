from math import sqrt, floor
from random import random

class RSA:
    def __init__(self):
        self.p = self.primeGen()
        self.q = self.primeGen()
        self.e = self.primeRelGen(self.phi())
        self.public_key = self.public_key_gen()
        self.private_key = self.private_key_gen()
        print(f"p = {self.p}")
        print(f"q = {self.q}")
        print(f"e = {self.e}")
        print(f"public_key = {self.public_key}")
        print(f"private_key = {self.private_key}")

    def phi(self):
        return (self.p - 1) * (self.q - 1)

    def primeGen(self):
        primes = [2]
        maximum = 1000
        for num in range(3, maximum, 2):
            is_prime = True
            square_root = sqrt(num)
            for prime in primes:
                if num % prime == 0:
                    is_prime = False
                    break
                if prime > square_root:
                    break
            if is_prime:
                primes.append(num)
        random_prime = primes[floor(random() * len(primes))]
        return random_prime

    def primeRelGen(self, phi):
        primes = [2]
        maximum = 1000
        for num in range(3, maximum, 2):
            is_prime = True
            square_root = sqrt(num)
            for prime in primes:
                if num % prime == 0:
                    is_prime = False
                    break
                if prime > square_root:
                    break
            if is_prime:
                if self.gcd(num, phi) > 1:
                    continue
                else:
                    primes.append(num)
        random_prime = primes[floor(random() * len(primes))]
        return random_prime

    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a % b)

    def modInverse(self, A, M):
        if self.gcd(A, M) > 1:
            # modulo inverse does not exist
            return -1
        for X in range(1, M):
            if (((A % M) * (X % M)) % M == 1):
                return X
        return -1

    def public_key_gen(self):
        n = self.p * self.q
        public_key = [self.e, n]
        return public_key

    def private_key_gen(self):
        n = self.p * self.q
        d = self.modInverse(self.e, self.phi())
        private_key = [d, n]
        return private_key

    def RSAEncrypt(self, msg, public_key):
        print(f"msg = {msg} - {type(msg)}")
        print(f"e= {public_key[0]} - {type(public_key[0])} || n={public_key[1]} - {type(public_key[1])}")
        encrypted = msg ** public_key[0] % public_key[1]
        return encrypted

    def RSADecrypt(self, encrypted, private_key):
        decrypted = encrypted ** private_key[0] % private_key[1]
        return decrypted