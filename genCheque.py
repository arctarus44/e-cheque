import sys
import os
import os.path
from rsa import RSA
from configparser import ConfigParser
import shutil
import tools

def read_invoice():
	"""Read an invoice from stdin and return an instance of ConfigParser."""
	filename = "tmp.txt"
	tmp_file = open(filename, 'w')
	for line in sys.stdin.readlines():
		tmp_file.write(line)
	tmp_file.close()
	invoice = ConfigParser()
	invoice.read(filename)
	os.remove("tmp.txt")
	return invoice

if __name__ == "__main__":
	real_drawer = sys.argv[1]
	invoice = read_invoice()
	tools.check_config(invoice, tools.STRCT_INVOICE)

	drawer = invoice[tools.SCT_I_INVOICE][tools.OPT_I_BUYER]
	total = invoice[tools.SCT_I_INVOICE][tools.OPT_I_TOTAL]
	payee = invoice[tools.SCT_I_INVOICE][tools.OPT_I_SELLER]
	transac_id = invoice[tools.SCT_I_INVOICE][tools.OPT_I_TRANS_ID]

	if drawer != real_drawer:
		print("This invoice is not for me !", sys.stderr)
		exit(1)

	# todo check if a check for this transaction was ever done
	cheque_fname = payee + "_" + transac_id + tools.EXT_CHEQUE
	cheque_fname = os.path.join(tools.DIR_CUSTOMERS, real_drawer,
								tools.DIR_CHQ_ISSUED, cheque_fname)
	if os.path.exists(cheque_fname) and os.path.isfile(cheque_fname):
		print("This invoice is already paid !", file=sys.stderr)
		exit(1)

	cheque_cp = ConfigParser()
	cheque_cp.add_section(tools.SCT_C_CHEQUE)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_DRAWER, drawer)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_TOTAL, total)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_PAYEE, payee)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_TRANS_ID, transac_id)

	with open(cheque_fname,'w') as cheque_f:
		cheque_cp.write(cheque_f)

	tmp = open(cheque_fname, 'r')
	print(tmp.read())

	# add some magic crypto here

	exit(0)
