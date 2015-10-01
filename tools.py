import binascii
import sys

ROLE_BANK = "Bank"
ROLE_SELLER = "Seller"

#######################################################
# Every name of section and option must be write here #
#######################################################
# Cheque file
SCT_C_CLIENT = "Client"
OPT_C_NAME = "Drawer"
OPT_C_AMOUNT = "Amount"
OPT_C_PAYEE = "Payee"
OPT_C_TRANS_ID = "Transaction_id"

# Key file
SCT_K_KEY = "Key"
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
FILE_PUB_KEY = "public.key"
FILE_PRI_KEY = "private.key"
FILE_PUB_SIGN = "public.sign"
FILE_SELLER_DB = "seller.db"
FILE_BANK_DB = "bank.db"



def text_to_int(text):
	"""Convert the ascii text given as string to an integer"""
	hex_repr = binascii.hexlify(text.encode("ascii"))
	return int(hex_repr.decode("ascii"), 16)

def int_to_text(integer):
	"""Convert the given number as an asciistring """
	hex_repr = hex(integer)[2:]	# skipping the 0x
	if len(hex_repr) % 2 != 0:
		hex_repr = "0" + hex_repr
	return binascii.unhexlify(hex_repr).decode("ascii")

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
