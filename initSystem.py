from rsa import RSA
import os
import os.path
import sys
import shutil
from configparser import  ConfigParser
from tools import *

DONE = "\033[1m\033[32mDone\033[0m"

def sign_customer_key(rsa, customer):
	"""Sign the public key of the customer with the rsa private key of
	the bank and put the result in a configuration file like this one
	[Bank]
	signature=232345478290189289289082907892017892789
	"""
	filename = "public.sign"
	customer_key = open(os.path.join("bank", customer, "public.key"), 'r')
	key_content = customer_key.read()[:-1]
	signature = rsa.sign(text_to_int(key_content))
	signature_file = ConfigParser()
	signature_file["Bank"] = {"signature": signature}
	with open(os.path.join("customers", customer, filename), 'w') as signfile:
		signature_file.write(signfile)

def sign_seller_key(rsa):
	"""Sign the public key of the customer with the rsa private key of
	the bank and put the result in a configuration file like this one
	[Bank]
	signature=232345478290189289289082907892017892789
	"""
	filename = "public.sign"
	customer_key = open(os.path.join("bank", "seller", "public.key"), 'r')
	key_content = customer_key.read()[:-1]
	signature = rsa.sign(text_to_int(key_content))
	signature_file = ConfigParser()
	signature_file["Bank"] = {"signature": signature}
	with open(os.path.join("seller", filename), 'w') as signfile:
		signature_file.write(signfile)


if __name__ == "__main__":

	try:
		nb_customers = int(sys.argv[1])
	except IndexError:
		print("Missing argument", sys.stderr)
		exit(1)

	# Creating the bank
	print("Creation of the Bank ", end="",flush=True)
	os.mkdir("bank")
	keys = RSA.generate_keys()#key_size=4096)
	RSA.store_key("bank", keys[RSA.private], keys[RSA.public])
	print(DONE)

	rsa_bank = RSA(keys[RSA.private][RSA.modulus],
				   d=keys[RSA.private][RSA.private_exponent])

	# Creating customer
	os.mkdir("customers")
	for i in range(0, nb_customers):
		try:
			customer = sys.argv[2+i]
		except IndexError:
			print("Missing customer name", sys.stderr)

		print("Creation of the customer " + customer, end=" ",flush=True)
		directory = os.path.join("customers", customer)
		os.mkdir(directory)

		# Generating the keys of the customer
		keys = RSA.generate_keys(key_size=1024)
		RSA.store_key(directory, keys[RSA.private], keys[RSA.public])

		# Adding the customer's public key in the bank directory
		customer_bank = os.path.join("bank", customer)
		os.mkdir(customer_bank)
		shutil.copy(os.path.join(directory, "public.key"), customer_bank)

		# Signing the customer's key with the bank private key
		sign_customer_key(rsa_bank, customer)
		print(DONE)

	#Creating the seller
	print("Creation of the Seller ", end="",flush=True)
	os.mkdir("seller")
	keys = RSA.generate_keys(key_size=1024)
	RSA.store_key("seller", keys[RSA.private], keys[RSA.public])

	os.mkdir("bank/seller")
	shutil.copy(os.path.join("seller", "public.key"), os.path.join("bank", "seller", "public.key"))
	sign_seller_key(rsa_bank)
	print(DONE)
