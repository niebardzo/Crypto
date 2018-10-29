#
# Implementation of RSA
#
# Author: Patryk Bogusz
#
#

"""

The keys for the RSA algorithm are generated the following way:

- Choose two distinct prime numbers p and q.
- For security purposes, the integers p and q should be chosen at random, and should be similar in magnitude but differ in length by a few digits to make factoring harder.[2] Prime integers can be efficiently found using a primality test.
- Compute n = pq.
- n is used as the modulus for both the public and private keys. Its length, usually expressed in bits, is the key length.
- Compute λ(n) = lcm(λ(p), λ(q)) = lcm(p − 1, q − 1), where λ is Carmichael's totient function. This value is kept private.
- Choose an integer e such that 1 < e < λ(n) and gcd(e, λ(n)) = 1; i.e., e and λ(n) are coprime.
- Determine d as d ≡ e−1 (mod λ(n)); i.e., d is the modular multiplicative inverse of e (modulo λ(n)).
- This is more clearly stated as: solve for d given d⋅e ≡ 1 (mod λ(n)).
- e having a short bit-length and small Hamming weight results in more efficient encryption – most commonly e = 216 + 1 = 65,537. However, much smaller values of e (such as 3) have been shown to be less secure in some settings.[14]
- e is released as the public key exponent.
- d is kept as the private key exponent.
- The public key consists of the modulus n and the public (or encryption) exponent e. The private key consists of the private (or decryption) exponent d, which must be kept secret. p, q, and λ(n) must also be kept secret because they can be used to calculate d.

"""


import random


def modular_pow(base, exponent, modulus):
	"""Source: https://en.wikipedia.org/wiki/Modular_exponentiation"""
	if modulus == 1:
		return 0
	c = 1
	for i in range(0, exponent):
		c = (c * base) % modulus
	return c


def is_prime(number):
	"""The function is checking if the number is prime or not. Source: https://en.wikipedia.org/wiki/Primality_test"""
	if number <= 1:
		return False
	elif number <= 3:
		return True
	elif number % 2 == 0 or number % 3 == 0:
		return False
	i = 5
	while i * i  <= number:
		if number % i == 0 or number % (i+2) == 0:
			return False
		i = i + 6
	return True


def random_primes(length):
	"""Fuction that generates to random prime numbers based on stated key_lenght"""
	number_range = range(1 << (length // 2 - 1),1 << (length // 2 + 1) )
	p = random.choice(number_range)
	q = random.choice(number_range)
	while not is_prime(p):
		p = random.choice(number_range)
	while not is_prime(q) and p != q:
		q = random.choice(number_range)
	return (p,q)


def are_coprimes(a, b):
	"""Functiom checks if two numbers a and b are coprime"""
	for n in range(2, min(a,b)+1):
		if a % n == 0 and b % n == 0:
			return False
	return True


def generate_pair_of_keys(length):
	"""Function which generates public and private keys"""
	p, q = random_primes(length)
	n = p * q
	lambd = lcm(p-1, q-1)
	for e in range(3, lambd, 2):
		if is_prime(e) and are_coprimes(e, lambd):
			break
	for d in range(3, lambd, 2):
		if d * e % lambd == 1:
			break
	return Public_key(n,e), Private_key(n, d)


def gcd(a, b):
	""" Euclid's algotith implementation. Source: https://en.wikipedia.org/wiki/Greatest_common_divisor"""
	while(b):
		a, b = b, a % b

	return a


def lcm(a, b):
	"""Least Common Multiple. Souce: https://en.wikipedia.org/wiki/Least_common_multiple"""
	return ((a*b)//gcd(a,b))


class Public_key:
	def __init__(self, n, e):
		self.e = e
		self.n = n


	def encrypt(self, message):
		return [modular_pow(ord(letter), self.e, self.n) for letter in message]


class Private_key:
	def __init__(self, n, d):
		self.d = d
		self.n = n


	def decrypt(self, encrypted_message):
		return ''.join([chr(modular_pow(letter, self.d, self.n)) for letter in encrypted_message])


try:
	length = input("What is the key length? ")
	if length.isalpha():
		raise ValueError
	public, private = generate_pair_of_keys(int(length))
	message = input("Type message: ")
	if not message.isalpha():
		raise ValueError
	encrypted = public.encrypt(str(message))
	print(''.join(map(lambda x: str(x), encrypted)))
	print(private.decrypt(encrypted))
	
except ValueError:
	print("Cannot Proceed.")