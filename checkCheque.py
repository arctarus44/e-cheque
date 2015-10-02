import sys
import os
import os.path
from configparser import ConfigParser
import tools

def exist_invoice(buyer, transac_id):
	"""Check if a transaction exist with the specified buyer and transaction
	id."""
	fname = buyer + "_" + transac_id + tools.EXT_INVOICE
	fname = os.path.joint(tools.DIR_SELLER, tools.DIR_INVOICE, fname)
	if os.path.isfile(fname):
		return True
	return False


if __name__ == "__main__":
	NO_INVOICE = "No invoice corresponding to the seller {0} and the transaction id {1}."
	cheque_cp = tools.read_stdin()
	tools.check_config(cheque_cp, tools.STRCT_CHEQUE)

	buyer = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_C_DRAWER]
	total = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_I_TOTAL]
	seller = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_I_PAYEE]
	transac_id = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_I_TRANS_ID]

	if not exist_invoice(buyer, transac_id):
		print(NO_INVOICE.format(buyer, transac_id), file=sys.stderr)
		exit(1)

	# Todo change the following line when a correct signature scheme will
	# be implemented
	cheque_cp[tools.ROLE_SELLER] = {"Valid" : "true"}
	fname = buyer + "_" + transac_id + tools.EXT_INVOICE
	fname = os.path.joint(tools.DIR_SELLER, tools.DIR_INVOICE, fname)
	with open(fname, 'w') as cheque_f:
		cheque_cp.write(cheque_f
