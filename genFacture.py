import configparser
import sys
import os
import random

SEED_LENGTH = 10
TRANSACTION_ID_LENGTH = 256

def genFacture(name,amount,to):

	config = configparser.RawConfigParser()
	random.seed(os.urandom(SEED_LENGTH))
	id_transac = hex(random.getrandbits(TRANSACTION_ID_LENGTH))
	config['CLIENT'] = {'Name' : name, 'Amount' : amount, 'To' : to, 'Transaction' : id_transac}
	with open('seller/facture_'+id_transac+'.ini','w') as facture:
		config.write(facture)
		facture.close()
	os.rename('seller/facture_'+id_transac+'.ini','customers/'+name+'/facture_'+id_transac+'.ini')

if __name__ == "__main__":
	genFacture(sys.argv[1],sys.argv[2],sys.argv[3])
