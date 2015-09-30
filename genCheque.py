import sys
from rsa import RSA
from configparser import ConfigParser

user_name = sys.argv[1]
def read_bill():
	"""Read a check from stdin and return an instance of ConfigParser."""
#	f = sys.stdin.readlines()
#os.path.join
	bill = ConfigParser()
	bill.read_file('/customers/'+user_name+'/facture.ini')
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

	if bill.get("CLIENT", "Name") != user_name:
		print("This cheque is not for me !", sys.stderr)
		exit(1)

	cheque = ConfigParser()
	cheque.add_section("cheque")
	cheque.set("cheque", "depositor", user_name)
	cheque.set("cheque", "beneficiary", bill.get("CLIENT", "To"))
	cheque.set("cheque", "amount", bill.get("CLIENT", "Amount"))
	cheque.set("cheque", "transaction_id", bill.get("CLIENT", "Transaction"))
	with open('customers/'+user_name+'/cheque.ini','w') as cheque:
		config.write(cheque)
		cheque.close()
	os.rename('customers/'+user_name+'/cheque.ini', 'seller/cheque.ini')	
	exit(0)
