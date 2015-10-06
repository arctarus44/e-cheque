import sys
import os
import os.path
import tools
from configparser import ConfigParser
from configparser import ParsingError
from rsa import RSA

def exist_invoice(buyer, transac_id):
	"""Check if a transaction exist with the specified buyer and transaction
	id."""
	fname = buyer + "_" + transac_id + tools.EXT_INVOICE
	fname = os.path.join(tools.DIR_SELLER, tools.DIR_INVOICE, fname)
	if os.path.isfile(fname):
		return True
	return False

def decode_sign(sign, drawee):
	"""Decode the signature and return a ConfigParser of the decoded
	signature. If the decoded message is not a correct check, exit"""

	# Retrieve the drawee public key
	puk_s_fname = os.path.join(tools.DIR_CUSTOMERS, drawee, tools.FILE_PUB_SIGN)
	prk_fname = os.path.join(tools.DIR_BANK, tools.FILE_PUB_KEY)
	pub_f = tools.decode_public_key(puk_s_fname, prk_fname, tools.ROLE_BANK)

	pub_k = RSA(int(pub_f[tools.SCT_K_KEY][tools.OPT_K_N]),
				e=int(pub_f[tools.SCT_K_KEY][tools.OPT_K_E]))

	decoded = pub_k.check_signature(sign)

	tmp = open(tools.TMP_FILE, 'w')
	tmp.write(decoded)
	tmp.close()

	# Parse the decoded cheque and check his structure
	decoded_cheque = ConfigParser()
	decoded_cheque.read(tools.TMP_FILE)
	os.remove(tools.TMP_FILE)
	tools.check_config(decoded_cheque, tools.STRCT_CHEQUE)
	return decoded_cheque

if __name__ == "__main__":
	NO_INVOICE = "No invoice corresponding to the seller {0}"
	NO_INVOICE += " and the transaction id {1}."

	try:
		sign_cp = tools.read_stdin()
	except ParsingError:
		print(tools.DRAWEE_SIGN_ERROR, file=sys.stderr)
		exit(1)
	drawee = sign_cp.sections()[0]

	cheque_cp = decode_sign(sign_cp[drawee][tools.OPT_S_SIGN], drawee)

	buyer = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_C_DRAWER]
	total = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_C_TOTAL]
	seller = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_C_PAYEE]
	transac_id = cheque_cp[tools.SCT_C_CHEQUE][tools.OPT_I_TRANS_ID]

	if not exist_invoice(buyer, transac_id):
		print(NO_INVOICE.format(buyer, transac_id), file=sys.stderr)
		exit(1)

	with open(tools.TMP_FILE, 'w') as cheque_f:
		cheque_cp.write(cheque_f)

	pri_f = ConfigParser()
	pri_f.read(os.path.join(tools.DIR_SELLER, tools.FILE_PRI_KEY))

	pri_k = RSA(int(pri_f[tools.SCT_K_KEY][tools.OPT_K_N]),
				d=int(pri_f[tools.SCT_K_KEY][tools.OPT_K_D]))

	with open(tools.TMP_FILE, 'w') as f:
		sign_cp.write(f)
	cheque_f = open(tools.TMP_FILE, 'r')
	content = cheque_f.read()
	os.remove(tools.TMP_FILE)

	content_signed = pri_k.sign(content)

	valide_cheque = ConfigParser()
	valide_cheque[tools.ROLE_SELLER] = {tools.OPT_S_SIGN: content_signed}
	valide_cheque.write(sys.stdout)
