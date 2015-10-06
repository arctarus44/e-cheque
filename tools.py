import binascii
import sys
import os
import rsa
from configparser import ConfigParser

TMP_FILE = "tmp.txt"

#########
# ROLES #
#########
ROLE_BANK = "Bank"
ROLE_SELLER = "Seller"

#######################################################
# Every name of section and option must be write here #
#######################################################
# Cheque file
SCT_C_CHEQUE = "Cheque"
OPT_C_DRAWER = "Drawer"
OPT_C_TOTAL = "Total"
OPT_C_PAYEE = "Payee"
OPT_C_TRANS_ID = "Transaction_id"

# Key file
SCT_K_KEY = "Key"
OPT_K_SIZE = "Size"
OPT_K_E = "E"
OPT_K_N = "N"
OPT_K_D = "D"

# Invoice
SCT_I_INVOICE = "Invoice"
OPT_I_TOTAL = "Total"
OPT_I_SELLER = "Seller"
OPT_I_TRANS_ID = "Transaction_id"
OPT_I_BUYER = "Buyer"

# Seller database
SCT_SD_PAY = "Pay_in"
SCT_SD_NOT_PAY = "Not_pay_in"

# Signature file
OPT_S_SIGN = "Signature"


#############################################
# Every parts of path name must be put here #
#############################################
DIR_BANK = "bank"
DIR_CUSTOMERS = "customers"
DIR_CHQ_ISSUED = "issued"
DIR_SELLER = "seller"
DIR_INVOICE = "invoices"
FILE_PUB_KEY = "public.key"
FILE_PRI_KEY = "private.key"
FILE_PUB_SIGN = "public.sign"
FILE_SELLER_DB = "seller.db"
FILE_BANK_DB = "bank.db"
EXT_INVOICE = ".inv"
EXT_CHEQUE = ".chq"

#################################################################
# Every structure of files open with ConfigParser must put here #
#################################################################
STRCT_INVOICE = {SCT_I_INVOICE: [OPT_I_TOTAL,
								 OPT_I_SELLER,
								 OPT_I_TRANS_ID,
								 OPT_I_BUYER]}

STRCT_CHEQUE = {SCT_C_CHEQUE: [OPT_C_DRAWER,
							   OPT_C_TOTAL,
							   OPT_C_PAYEE,
							   OPT_C_TRANS_ID]}

STRCT_PUB_KEY = {SCT_K_KEY: [OPT_K_E,
							 OPT_K_N]}

STRCT_PRI_KEY = {SCT_K_KEY: [OPT_K_D,
							 OPT_K_N]}


def check_config(config, structure):
	"""Check if the ConfigParser instance respect the structure required."""

	MISSING_SCT = "Missing section {0}."
	MISSING_OPT = "Missing option {0} in section {1}."

	for sect_name in structure.keys():
		section = structure[sect_name]
		try:
			conf_section = config[sect_name]
		except KeyError:
			print(MISSING_SCT.format(sect_name), file=sys.stderr)
			return False
		for option in section:
			try:
				conf_section[option]
			except KeyError:
				print(MISSING_OPT.format(option, sect_name), file=sys.stderr)
				return False
	return True


def read_stdin():
	"""Read a file from stdin and return an instance of ConfigParser
	corresponding to the file."""
	tmp_file = open(TMP_FILE, 'w')
	for line in sys.stdin.readlines():
		tmp_file.write(line)
	tmp_file.close()
	config = ConfigParser()
	config.read(TMP_FILE)
	os.remove(TMP_FILE)
	return config

def decode_public_key(pk_signed, public_key, name):
	"""Decode the public key signed by name with his private key."""
	pub_f = ConfigParser()
	pub_f.read(public_key)

	pub_k = rsa.RSA(int(pub_f[SCT_K_KEY][OPT_K_N]),
				e=int(pub_f[SCT_K_KEY][OPT_K_E]))

	puk_sign_f = open(pk_signed, 'r')
	content = puk_sign_f.read()
	puk_sign_f.close()

	tmp = open(TMP_FILE, 'w')
	tmp.write(content)
	tmp.close()

	content_cp = ConfigParser()
	content_cp.read(TMP_FILE)

	decoded_content = pub_k.check_signature(content_cp[name][OPT_S_SIGN])
	tmp = open(TMP_FILE, 'w')
	tmp.write(decoded_content)
	tmp.close()

	puk_cp = ConfigParser()
	puk_cp.read(TMP_FILE)
	os.remove(TMP_FILE)

	check_config(puk_cp, STRCT_PUB_KEY)
	return puk_cp
