from configparser import ConfigParser
import sys
import os
import os.path
import random
from shutil import copyfile
import tools

SEED_LENGTH = 10

TRANSACTION_ID_LENGTH = 256

# adding sign of the invoice  and the public key of the seller sign by the Bank
# to validate the invoice

def add_invoice_db(transac_id, total):
	"""Add the invoice in the seller database."""

	db_cp = ConfigParser()
	db_fname = os.path.join(tools.DIR_SELLER, tools.FILE_SELLER_DB)
	db_cp.read(db_fname)
	db_cp.set(tools.SCT_SD_NOT_PAY, transac_id, str(total))

	with open(db_fname,'w') as db_file:
		db_cp.write(db_file)


def gen_invoice(buyer, seller, total):

	# Generation of the transaction id
	random.seed(os.urandom(SEED_LENGTH))
	transac_id = hex(random.getrandbits(TRANSACTION_ID_LENGTH))[2:]

	add_invoice_db(transac_id, total)

	invoice_cp = ConfigParser()
	# Generate the invoice
	invoice_cp.add_section(tools.SCT_I_INVOICE)
	invoice_cp[tools.SCT_I_INVOICE] = {tools.OPT_I_SELLER: tools.ROLE_SELLER,
									   tools.OPT_I_BUYER: buyer,
									   tools.OPT_I_TOTAL: total,
									   tools.OPT_I_TRANS_ID: transac_id}

	invoice_fname = buyer + "_" + transac_id + tools.EXT_INVOICE

	invoice_fname = os.path.join(tools.DIR_SELLER, tools.DIR_INVOICE,
								 invoice_fname)
	with open(invoice_fname, 'w') as invoice_file:
		invoice_cp.write(invoice_file)

	invoice = open(invoice_fname, 'r')
	invoice_content = invoice.read()
	invoice.close()
	print(invoice_content)

def parse_argt():
	buyer = sys.argv[1]
	seller = sys.argv[2]
	total = int(sys.argv[3])
	return buyer, seller, total

if __name__ == "__main__":
	buyer, seller, total = parse_argt()
	gen_invoice(buyer, seller, total)
