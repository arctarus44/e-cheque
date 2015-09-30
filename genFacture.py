import configparser
import sys
import os
import random
from datetime import datetime, date, time

SEED_LENGTH = 10

TRANSACTION_ID_LENGTH = 256

def genFacture(name,amount,to):

	config = configparser.RawConfigParser()
	random.seed(os.urandom(SEED_LENGTH))
	
	dt = datetime.now()
	dn = str(dt.year) + str(dt.month) + str(dt.day) + str(dt.hour) + str(dt.minute) + str(dt.second) + str(dt.microsecond)
	id_transac = hex(random.getrandbits(TRANSACTION_ID_LENGTH))[2:]

	config['CLIENT'] = {'Name' : name, 'Amount' : amount, 'To' : to, 'Transaction' : id_transac}
	with open('seller/facture_'+id_transac+'_'+dn+'.ini','w') as facture:
		config.write(facture)
		facture.close()
	
	os.path.join("seller",'facture_'+id_transac+'_'+dn+'.ini')
	facture = open('seller/facture_'+id_transac+'_'+dn+'.ini','r')
	fr = facture.read()
	print(fr)
	facture.close()
	

if __name__ == "__main__":
	genFacture(sys.argv[1],sys.argv[2],sys.argv[3])
