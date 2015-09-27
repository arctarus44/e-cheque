import os
import sys
import os.path

import math
import random
from fractions import gcd

# todo in is_prime use Miller–Rabin primality test
def is_prime(p):
	"""Check if the number p is a prime number."""
	if p == 1:
		return False
	if p == 2:
		return True
	if p % 2 == 0:
		return False
	if p % 10 == 5:
		return False

	p_str = str(p)
	sum_digits = 0
	for digit_str in p_str:
		sum_digits += int(digit_str)
	if sum_digits % 3 == 0:
		return False

	sqr = math.sqrt(p)
	cpt = 3
	while(cpt <= sqr):
		if(p % cpt == 0):
			return False
		cpt += 2

	return True

def compute_big_prime(size=2048):
	"""Return a big prime number. If you want to change the size of
	prime number, you can change the size parameter."""
	while True:
		prime = random.getrandbits(size)
		if is_prime(prime):
			return prime

def extended_gcd(aa, bb):
	lastremainder, remainder = abs(aa), abs(bb)
	x, lastx, y, lasty = 0, 1, 1, 0
	while remainder:
		lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
		x, lastx = lastx - quotient*x, x
		y, lasty = lasty - quotient*y, y
	return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


class RSA:
	"""Implement the RSA cryptosystem."""

	modulus = "N"
	public_exponent = "E"
	private_exponent = "D"
	private = "PRIVATE"
	public = "PUBLIC"

	@staticmethod
	def read_keys(user, dir, instanciate=True):
		"""Read the the public key of an user in a directory. If instanciate
		is set to true (the default behaviour), this method will return
		an instance of RSA."""
		if instanciate:
			pass
		return {RSA.private:{},
		RSA.public:{}}

	@staticmethod
	def generate_keys():
		"""Generate the public and private keys to use with RSA."""
		p = compute_big_prime(size = 1024)
		q = compute_big_prime(size = 1024)
		n = p * q
		phi_n = p - 1 * q - 1

		e = random.randrange(1, phi_n)
		while gcd(e, phi_n) != 1:
			e = random.randrange(1, phi_n)

		d = modinv(e, phi_n)
		private_dict = {RSA.private_exponent: d, RSA.modulus: n}
		public_dict = {RSA.public_exponent: e, RSA.modulus: n}
		return {RSA.private: private_dict, RSA.public: public_dict}

	@staticmethod
	def store_key(directory, private_dict=None, public_dict=None):
		"""Store the private and/or the public key store as a dict into files
		in the given directory.
		The public key will be store under the file public.key and the private
		key will be store under the file private key."""

		from configparser import ConfigParser

		private_file = "private.key"
		public_file = "public.key"

		if private_dict is not None:
			private_k = ConfigParser()
			private_k["key"] = private_dict
			with open(os.path.join(directory, private_file), 'w') as keyfile:
				private_k.write(keyfile)

		if public_dict is not None:
			public_k = ConfigParser()
			public_k["key"] = public_dict
			with open(os.path.join(directory, public_file), 'w') as keyfile:
				public_k.write(keyfile)


	def __init__(self, n, d, e):
		self.__n = n
		self.__d = d
		self.__e = e

	def decryption(self, c):
		return pow(c, self.__d, self.__n)

	def encryption(self, m):
		return pow(m, self.__e, self.__n)

	def sign(self, m):
		return pow(m, self.__d, self__n)

	def check_signature(self, s):
		"""This method do not realy chek if the signature is rigth. This method
		cannot check if the result is right or not. It return the content
		decoded from the signature."""
		return pow(s, self.__e, self.__n)