import sys
import os
from rsa import RSA
from configparser import ConfigParser
<<<<<<< HEAD
from shutil import copyfile

def read_bill():
	"""Read a check from stdin and return an instance of ConfigParser."""
	filename = "tmp.txt"
	tmp_file = open(filename, 'w')
	for line in sys.stdin.readlines():
		tmp_file.write(line)
	tmp_file.close()
	bill = ConfigParser()
	bill.read(filename)
	os.remove("tmp.txt")
	return bill

if __name__ == "__main__":
	bill = read_bill()

	if not bill.has_section("CLIENT"):
		print("Missing section client", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "Name"):
		print("Missing option name in the client section", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "Amount"):
		print("Missing option amount in the client section", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "To"):
		print("Missing option ordre in the client section", file=sys.stderr)
		exit(1)
	if not bill.has_option("CLIENT", "Transaction"):
		print("Missing option transaction in the client section", file=sys.stderr)
		exit(1)

	customer_name = bill["CLIENT"]["name"]

	if bill.get("CLIENT", "Name") != customer_name:
		print("This cheque is not for me !", sys.stderr)
		exit(1)

	cheque = ConfigParser()
	cheque.add_section("cheque")
	cheque.set("cheque", "depositor", customer_name)
	cheque.set("cheque", "beneficiary", bill.get("CLIENT", "To"))
	cheque.set("cheque", "amount", bill.get("CLIENT", "Amount"))
	cheque.set("cheque", "transaction_id", bill.get("CLIENT", "Transaction"))
	cheque_fname = 'customers/' + customer_name + '/writed/cheque_' + bill["CLIENT"]["To"]+ "_" + bill["CLIENT"]["Transaction"] + '.ini'
	with open(cheque_fname,'w') as cheque_file:
		cheque.write(cheque_file)
	copyfile(cheque_fname, 'seller/cheque.ini')
	tmp = open(cheque_fname, 'r')
	print(tmp.read())
	exit(0)
