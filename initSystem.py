from rsa import RSA
import os
import os.path
import sys
import shutil

DONE = "\033[1m\033[32mDone\033[0m"


if __name__ == "__main__":

	try:
		nb_customers = int(sys.argv[1])
	except IndexError:
		print("Missing argument", sys.stderr)
		exit(1)

	# Creating the bank
	print("Creation of the Bank ", end="",flush=True)
	os.mkdir("bank")
	keys = RSA.generate_keys()
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
		keys = RSA.generate_keys()
		RSA.store_key(directory, keys[RSA.private], keys[RSA.public])

		# Adding the customer's public key in the bank directory
		customer_bank = os.path.join("bank", customer)
		os.mkdir(customer_bank)
		shutil.copy(os.path.join(directory, "public.key"), customer_bank)

		# todo : Signing the customer's key with the bank private key

		print(DONE)

	#Creating the seller
	print("Creation of the Seller ", end="",flush=True)
	os.mkdir("seller")
	keys = RSA.generate_keys()
	RSA.store_key("seller", keys[RSA.private], keys[RSA.public])
	print(DONE)
