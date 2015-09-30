import os
import sys
from initSystem import *

if __name__ == "__main__":
#	1. Le client C fait chiffrer sa clé publique par sa banque B qui utilise sa clé privée pour le chiffrement.
#	La banque conserve la clé publique du client et lui retourne le résultat.
	initSystem()

#	2. Le client C veut acheter un bien à un vendeur V. Le vendeur lui fourni une facture
#	avec un ordre, un montant à payer, et un numéro aléatoire.
	genFacture
	
#	3. Le client C émet un chèque contenant le nom du client, le montant à payer, l'ordre et le numéro aléatoire.
#	Le client envoie en même temps sa clé publique chiffrée par la banque B.
	genCheque
	
#	4. Le vendeur V vérifie que le numéro aléatoire, l'ordre et le montant correspondent à une facture déjà éditée.
#	Sinon le vendeur refuse le chèque.

#	5. Le vendeur V chiffre le chèque avec sa clé privée. Il fournit le résultat à la banque avec sa clé publique.

#	6. La banque vérifie que le chèque a bien été chiffré par le vendeur en le déchiffrant avec sa clé publique.
#	Elle vérifie que le document déchiffré correspond bien à un chèque d'un client en déchiffrant
#	la partie chiffrée du chèque avec la clé publique du client.
#	Elle compare les valeurs obtenues avec les valeurs contenues dans la partie non chiffrée du chèque.
	exit(0)

