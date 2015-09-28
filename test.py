from configparser import ConfigParser
from rsa import RSA
from tools import *

if __name__ == "__main__":
	sign_file = ConfigParser()
	sign_file.read("customers/pierre/public.sign")
	sign = sign_file["Bank"]["signature"]

	pu_bank_file = ConfigParser()
	pu_bank_file.read("bank/public.key")
	rsa_bank = RSA(int(pu_bank_file["key"]["n"]), e=int(pu_bank_file["key"]["e"]))

	int_to_text(rsa_bank.check_signature(int(sign)))
