import configparser
import sys
import os
import random

SEED_LENGTH = 10
TRANSACTION_ID_LENGTH = 256

def genFacture(name,price,to):

	config = configparser.RawConfigParser()
	random.seed(os.urandom(SEED_LENGTH))
	config['CLIENT'] = {'Name' : name, 'Price' : price, 'To' : to, 'Transaction' : random.getrandbits(TRANSACTION_ID_LENGTH)}
	with open('facture.ini','w') as facture:
		config.write(facture)

if __name__ == "__main__":
	genFacture(sys.argv[1],sys.argv[2],sys.argv[3])
