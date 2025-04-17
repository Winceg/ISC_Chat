from math import sqrt, floor, gcd
from random import random, randint


class PrimeStuff:

    @staticmethod
    def primeGen():
        primes = [2]
        maximum = 500
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
        maximum = 500
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

    @staticmethod
    def get_prime_factors(n):
        """Return the list of prime factors of n"""
        factors = set()
        i = 2
        while i * i <= n:
            while n % i == 0:
                factors.add(i)
                n //= i
            i += 1
        if n > 1:
            factors.add(n)
        return list(factors)

    @staticmethod
    def is_primitive_root(g, p):
        """Check if g is a primitive root modulo p"""
        if gcd(g, p) != 1:
            return False
        phi = p - 1
        factors = PrimeStuff.get_prime_factors(phi)
        for q in factors:
            if pow(g, phi // q, p) == 1:
                return False
        return True

    @staticmethod
    def generate_primitive_root(p):
        """Generate a random primitive root modulo prime p"""
        if p < 3:
            raise ValueError("p must be a prime greater than 2")
        while True:
            g = randint(2, p - 2)
            if PrimeStuff.is_primitive_root(g, p):
                return g
