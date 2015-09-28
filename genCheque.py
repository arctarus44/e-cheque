import sys
from rsa import RSA
from configparser import ConfigParser

def read_bill():
	"""Read a check from stdin and return an instance of ConfigParser."""
	f = sys.stdin.readlines()
	bill = ConfigParser()
	bill.read_file(f)
	return bill

if __name__ == "__main__":
	bill = read_bill()
	user_name = sys.argv[1]

	if not bill.has_section("CLIENT"):
		print("Missing section client", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "nom"):
		print("Missing option name in the client section", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "montant"):
		print("Missing option amount in the client section", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "ordre"):
		print("Missing option ordre in the client section", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "transaction"):
		print("Missing option transaction in the client section", file=sys.stderr)
		exit(1)

	if bill.get("CLIENT", "nom") != user_name:
		print("This cheque is not for me !", sys.stderr)
		exit(1)

	cheque = ConfigParser()
	cheque.add_section("cheque")
	cheque.set("cheque", "depositor", user_name)
	cheque.set("cheque", "beneficiary", bill.get("CLIENT", "To"))
	cheque.set("cheque", "amount", bill.get("CLIENT", "Amount"))
	cheque.set("cheque", "transaction_id", bill.get("CLIENT", "transaction"))
