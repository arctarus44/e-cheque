import binascii
import sys
import os
from configparser import ConfigParser


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
OPT_K_N = "D"
OPT_K_D = "N"

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
	filename = "tmp.txt"
	tmp_file = open(filename, 'w')
	for line in sys.stdin.readlines():
		tmp_file.write(line)
	tmp_file.close()
	config = ConfigParser()
	config.read(filename)
	os.remove("tmp.txt")
	return config
