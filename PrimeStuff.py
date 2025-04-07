from math import sqrt, floor
from random import random


class PrimeStuff:

    @staticmethod
    def primeGen():
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

    @staticmethod
    def primeRelGen(phi):
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
                if PrimeStuff.gcd(num, phi) > 1:
                    continue
                else:
                    primes.append(num)
        random_prime = primes[floor(random() * len(primes))]
        return random_prime

    @staticmethod
    def gcd(a, b):
        if b == 0:
            return a
        return PrimeStuff.gcd(b, a % b)

    @staticmethod
    def modInverse(A, M):
        if PrimeStuff.gcd(A, M) > 1:
            # modulo inverse does not exist
            return -1
        for X in range(1, M):
            if (((A % M) * (X % M)) % M == 1):
                return X
        return -1
