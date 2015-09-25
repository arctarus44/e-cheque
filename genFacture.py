import configparser
import sys

def genFacture(nom,montant,ordre):

	config = configparser.RawConfigParser()
	config['CLIENT'] = {'Nom' : nom, 'Montant' : montant, 'Ordre' : ordre}
	with open('facture.txt','w') as facture:
		config.write(facture)

if __name__ == "__main__":
	genFacture(sys.argv[1],sys.argv[2],sys.argv[3])
