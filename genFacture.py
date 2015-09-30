import configparser
import sys
import os
import random

SEED_LENGTH = 10
TRANSACTION_ID_LENGTH = 1024

def genFacture(name,amount,to):

	config = configparser.RawConfigParser()
	random.seed(os.urandom(SEED_LENGTH))
	config['CLIENT'] = {'Name' : name, 'Amount' : amount, 'To' : to, 'Transaction' : hex(random.getrandbits(TRANSACTION_ID_LENGTH))}
	with open('seller/facture.ini','w') as facture:
		config.write(facture)
		facture.close()
	os.rename('seller/facture.ini','customers/'+name+'/facture.ini')

if __name__ == "__main__":
	genFacture(sys.argv[1],sys.argv[2],sys.argv[3])
