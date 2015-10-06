from rsa import RSA
import os
import os.path
import sys
import shutil
from configparser import  ConfigParser
import tools

DONE = "\033[1m\033[32mDone\033[0m"

def sign_key(rsa, key, dest):
	"""Sign the key with the instance of RSA public key and store the result
	in the dest directory"""
	if os.path.isdir(dest) is False:
		raise NotADirectoryError()
	if os.path.isfile(key) is False:
		raise IsADirectoryError()

	key = open(key, 'r')
	content = key.read()
	sign = rsa.sign(content)

	sign_cp = ConfigParser()
	sign_cp[tools.ROLE_BANK] = {tools.OPT_S_SIGN: str(sign)}
	with open(os.path.join(dest, tools.FILE_PUB_SIGN), 'w') as sign_f:
		sign_cp.write(sign_f)

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

		print("Creation of the customer " + customer, end=" ", flush=True)

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
		key_fname = os.path.join(directory, tools.FILE_PUB_KEY)
		sign_key(rsa_bank, key_fname, directory)
		# Copy of the signature in the customer's directory of the bank
		sign_f = os.path.join(tools.DIR_CUSTOMERS,
							  customer,
							  tools.FILE_PUB_SIGN)
		dest = os.path.join(tools.DIR_BANK, customer, tools.FILE_PUB_SIGN)
		shutil.copyfile(sign_f, dest)

		directory = os.path.join(directory, tools.DIR_CHQ_ISSUED)
		os.mkdir(directory)
		print(DONE)

	#Creation of the seller
	print("Creation of the Seller ", end="", flush=True)

	# Creation of the seller's directory
	os.mkdir(tools.DIR_SELLER)
	os.mkdir(os.path.join(tools.DIR_BANK, tools.DIR_SELLER))

	# Generation of seller's keys
	keys = RSA.generate_keys(key_size=1024)
	RSA.store_key(tools.DIR_SELLER, keys[RSA.private], keys[RSA.public])

	# Creation of the "bank account"
	os.mkdir(os.path.join(tools.DIR_SELLER, tools.DIR_INVOICE))

	# Copy the seller key to the "bank account"
	seller_pub_k = os.path.join(tools.DIR_SELLER, tools.FILE_PUB_KEY)
	dest = os.path.join(tools.DIR_BANK, tools.DIR_SELLER)
	shutil.copy(seller_pub_k, dest)

	# Sign the seller's public key
	sign_key(rsa_bank, seller_pub_k, tools.DIR_SELLER)

	# and copy it to his "bank account"
	sign_f = os.path.join(tools.DIR_SELLER,
						  tools.FILE_PUB_SIGN)
	dest = os.path.join(tools.DIR_BANK, tools.DIR_SELLER, tools.FILE_PUB_SIGN)
	shutil.copyfile(sign_f, dest)
	print(DONE)

	print("Creation of the databases ", end="", flush=True)
	bank_db = ConfigParser()
	for customer in customers_lst:
		bank_db.add_section(customer)
	bank_db_f = os.path.join(tools.DIR_BANK, tools.FILE_BANK_DB)
	with open(bank_db_f, 'w') as database_file:
		bank_db.write(database_file)

	seller_db = ConfigParser()
	seller_db.add_section(tools.SCT_SD_NOT_PAY)
	seller_db.add_section(tools.SCT_SD_PAY)

	seller_db_f = os.path.join(tools.DIR_SELLER, tools.FILE_SELLER_DB)
	with open(seller_db_f, 'w') as database_file:
		seller_db.write(database_file)
	print(DONE)
