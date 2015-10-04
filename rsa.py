import os
import sys
import os.path
import math
import random
from fractions import gcd
from configparser import ConfigParser


def is_prime(n, accuracy=10):
	"""Check if the number p is a prime number. Rabin-Miller edition.
	If you are 'bit' paranoid, you can use a bigger integer for accuracy.
	I choose accuracy = 10, because I think 1/4^10 is strong enough. But
	I am not a cryptography expert nor a mathematician."""
	if n <= 2:
		return False
	if n == 2:
		return True
	if n % 2 == 0:
		return False

	s = 0
	d = n-1

	while d % 2 == 0:
		s += 1
		d = d >> 1

	for i in range(0, accuracy):
		a = random.randint(2, n - 1)
		x = pow(a, d, n)
		if x != 1 and x != n - 1:
			for i in range(1, s):
				x = pow(x, 2, n)
				if x == 1:
					return False
				elif x == n - 1:
					a = 0
					break
			if a:
				return False
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
	__SPLIT_SIZE = 100
	__PADDING = "\0"

	@staticmethod
	def __text_to_int(text):
		"""Convert the ascii text given as string to an integer"""
		integer = 0
		for c in text:
			integer = integer << 8
			integer = integer + ord(c)
		return integer

	@staticmethod
	def __int_to_text(integer):
		"""Convert the given number as an asciistring """
		text = ""
		while integer>0:
			char = chr(integer & 0xFF)
			text = char + text
			integer = integer >> 8
		return text[:-1]

	@staticmethod
	def read_key(file, instanciate=True):
		"""Read the key. If instanciate is set to true
		(the default behaviour), this method will return an instance of RSA."""
		key_file = ConfigParser()
		key_file.read(file)
		key= {RSA.modulus: int(key_file["key"]["n"])}
		if key_file.has_option("key", "e"): # the key is a public key
			key[RSA.public_exponent] = int(key_file["key"]["e"])
			if instanciate:
				return RSA(key[RSA.modulus], e=key[RSA.public_exponent])

		else:					# the key is a private key
			key[RSA.private_exponent] = int(key_file["key"]["d"])
			if instanciate:
				return RSA(key[RSA.modulus], d=key[RSA.private_exponent])
		return key

	@staticmethod
	def generate_keys(key_size=1024):
		"""Generate the public and private keys to use with RSA."""
		p = compute_big_prime(size=key_size)
		q = compute_big_prime(size=key_size)
		n = p * q
		phi_n = (p - 1) * (q - 1)

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


	def __init__(self, n, d=None, e=None):
		self.__n = n
		self.__d = d
		self.__e = e

	def decryption(self, c):
		return pow(c, self.__d, self.__n)

	def encryption(self, m):
		return pow(m, self.__e, self.__n)

	def sign(self, m):
		if len(m) % self.__SPLIT_SIZE != 0: # need some padding
			for i in range(0, self.__SPLIT_SIZE - (len(m) % self.__SPLIT_SIZE) -1):
				m = m + self.__PADDING

		m = str(self.__text_to_int(m))
		m_split = [m[i:i+self.__SPLIT_SIZE]
				   for i in range(0, len(m), self.__SPLIT_SIZE)]

		result = []
		for part in m_split:
			res = pow(int(part), self.__d, self.__n)
			result.append(pow(int(part), self.__d, self.__n))
		return result

	def check_signature(self, sign):
		"""This method do not realy chek if the signature is rigth. This method
		cannot check if the result is right or not. It return the content
		decoded from the signature."""

		def add_padding(txt):
			"""Add some padding to the left"""
			for i in range(0, self.__SPLIT_SIZE - len(txt)):
				txt = "0" + txt
			return txt

		def remove_right_padding(text):
			count = 0
			for c in reversed(text):
				if c == self.__PADDING:
					count += 1
				if c != self.__PADDING:
					break
			return text[:-count]

		result = ""
		small = 0
		for s in sign:
			res = str(pow(int(s), self.__e, self.__n))
			if len(res) != self.__SPLIT_SIZE:
				small += 1
				res = add_padding(res)
			result += res
		txt = self.__int_to_text(int(result))
		return remove_right_padding(txt)
