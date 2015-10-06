import sys
import os
import os.path
from rsa import RSA
from configparser import ConfigParser
from configparser import ParsingError
import shutil
import tools

ALREADY_PAID = "This invoice is already paid !"
NOT_FOR_ME = "This invoice is not for me !"

def check_invoice(signed_invoice):
	"""Check if the configparser instance is a signed invoice. If not exit."""

	seller_sign_key = os.path.join(os.path.join(tools.DIR_SELLER,
												tools.FILE_PUB_SIGN))
	bank_pukf = os.path.join(tools.DIR_BANK, tools.FILE_PUB_KEY)

	pub_cp = tools.decode_public_key(seller_sign_key, bank_pukf,
									 tools.ROLE_BANK)

	tools.check_config(pub_cp, tools.STRCT_PUB_KEY)

	pub_k = RSA(int(pub_cp[tools.SCT_K_KEY][tools.OPT_K_N]),
				e=int(pub_cp[tools.SCT_K_KEY][tools.OPT_K_E]))

	check = pub_k.check_signature(signed_invoice[tools.ROLE_SELLER][tools.OPT_S_SIGN])

	tmp = open(tools.TMP_FILE, 'w')
	tmp.write(check)
	tmp.close()

	invoice_cp = ConfigParser()
	invoice_cp.read(tools.TMP_FILE)
	os.remove(tools.TMP_FILE)
	tools.check_config(invoice_cp, tools.STRCT_INVOICE)
	return invoice_cp

if __name__ == "__main__":
	try:
		real_drawer = sys.argv[1]
	except IndexError:
		print("You must give a customer name.", file=sys.stderr)
		exit(1)
	try:
		signed_inv = tools.read_stdin()
	except ParsingError:
		print(tool.SELLER_SIGN_ERROR, file=sys.stderr)
		exit(1)

	invoice = check_invoice(signed_inv)

	drawer = invoice[tools.SCT_I_INVOICE][tools.OPT_I_BUYER]
	total = invoice[tools.SCT_I_INVOICE][tools.OPT_I_TOTAL]
	payee = invoice[tools.SCT_I_INVOICE][tools.OPT_I_SELLER]
	transac_id = invoice[tools.SCT_I_INVOICE][tools.OPT_I_TRANS_ID]

	if drawer != real_drawer:
		print(NOT_FOR_ME, file=sys.stderr)
		exit(1)

	cheque_fname = payee + "_" + transac_id + tools.EXT_CHEQUE
	cheque_fname = os.path.join(tools.DIR_CUSTOMERS, real_drawer,
								tools.DIR_CHQ_ISSUED, cheque_fname)
	if os.path.exists(cheque_fname) and os.path.isfile(cheque_fname):
		print(ALREADY_PAID, file=sys.stderr)
		exit(1)

	cheque_cp = ConfigParser()
	cheque_cp.add_section(tools.SCT_C_CHEQUE)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_DRAWER, drawer)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_TOTAL, total)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_PAYEE, payee)
	cheque_cp.set(tools.SCT_C_CHEQUE, tools.OPT_C_TRANS_ID, transac_id)

	with open(cheque_fname,'w') as cheque_f:
		cheque_cp.write(cheque_f)

	cheque_f = open(cheque_fname, 'r')
	cheque_content = cheque_f.read()

	pri_cp = ConfigParser()
	pri_cp.read(os.path.join(tools.DIR_CUSTOMERS, real_drawer, tools.FILE_PRI_KEY))

	pri_k = RSA(int(pri_cp[tools.SCT_K_KEY][tools.OPT_K_N]),
				d=int(pri_cp[tools.SCT_K_KEY][tools.OPT_K_D]))

	sign = pri_k.sign(cheque_content)

	sign_cp = ConfigParser()
	sign_cp[real_drawer] = {tools.OPT_S_SIGN: str(sign)}
	sign_cp.write(sys.stdout)
