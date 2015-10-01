from rsa import RSA
import os
import os.path
import sys
import shutil
from configparser import  ConfigParser
import tools

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

def parsing_arguments():
	"""Return the list of customers. Exit if some are missing"""
	try:
		nb_customers = int(sys.argv[1])
	except IndexError:
		print("Missing argument", sys.stderr)
		exit(1)

	customers = []

	for i in range(0, nb_customers):
		try:
			customers.append(sys.argv[2+i])
		except IndexError:
			print("Missing customer name", sys.stderr)
			exit(1)

	return customers

if __name__ == "__main__":

	customers_lst = parsing_arguments()

	# Creating the bank
	print("Creation of the Bank ", end="",flush=True)

	os.mkdir(tools.DIR_BANK)
	keys = RSA.generate_keys()#key_size=4096)
	RSA.store_key(tools.DIR_BANK, keys[RSA.private], keys[RSA.public])
	print(DONE)

	rsa_bank = RSA(keys[RSA.private][RSA.modulus],
				   d=keys[RSA.private][RSA.private_exponent])

	# Creating the customers
	os.mkdir(tools.DIR_CUSTOMERS)
	customers_list = []
	for customer in customers_lst:

		print("Creation of the customer " + customer, end=" ",flush=True)

		# Creation of the customer's path
		directory = os.path.join(tools.DIR_CUSTOMERS, customer)
		os.mkdir(directory)

		# Generation of customer's keys
		keys = RSA.generate_keys(key_size=1024)
		RSA.store_key(directory, keys[RSA.private], keys[RSA.public])

		# Adding the customer's public key in the bank directory
		customer_bank = os.path.join(tools.DIR_BANK, customer)
		os.mkdir(customer_bank)
		shutil.copy(os.path.join(directory, tools.FILE_PUB_KEY), customer_bank)

		# Signing the customer's key with the bank private key
		sign_customer_key(rsa_bank, customer)

		directory = os.path.join(directory, tools.DIR_CHQ_ISSUED)
		os.mkdir(directory)
	print(DONE)

	#Creation of the seller
	print("Creation of the Seller ", end="",flush=True)
	os.mkdir(tools.DIR_SELLER)
	keys = RSA.generate_keys(key_size=1024)
	RSA.store_key(tools.DIR_SELLER, keys[RSA.private], keys[RSA.public])

	os.mkdir(os.path.join(tools.DIR_BANK, tools.DIR_SELLER))
	seller_pub_k = os.path.join(tools.DIR_SELLER, tools.FILE_PUB_KEY)
	dest = os.path.join(tools.DIR_BANK, tools.DIR_SELLER, tools.FILE_PUB_KEY)
	shutil.copy(seller_pub_k, dest)

	#todo create a function for seller and the customer
	sign_seller_key(rsa_bank)
	print(DONE)

	print("Creation of the databases ", end="",flush=True)
	bank_db = ConfigParser()
	for customer in customers_lst:
		bank_db.add_section(customer)
	bank_db_f = os.path.join(tools.DIR_BANK, tools.FILE_BANK_DB)
	with open(bank_db_f, 'w') as database_file:
		bank_db.write(database_file)

	seller_db = ConfigParser()
	seller_db.add_section(tools.SCT_SD_NOT_PAY)
	seller_db.add_section(tools.SCT_SD_PAY)

	seller_db_f = os.path.join(tools.DIR_SELLER, tools.DIR_SELLER_DB)
	with open(seller_db_f, 'w') as database_file:
		seller_db.write(database_file)
	print(DONE)
