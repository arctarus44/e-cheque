# e-cheque
##A system to write e-cheque.
###or a system to save the trees from the diabolical banks.

Utilisation :

Initialisation du système avec deux client
```sh
python initSystem.py 2 pierre paul
```

Génération d'une facture pour l'utilisateur pierre par le vendeur seller et d'un
montant de 200 :
```sh
python genInvoice.py pierre seller 200 > invoice.sign
```

Génération du chèque par l'utilisateur pierre en utilisant la facture généré
précédemment :
```sh
python genCheque.py pierre < invoice.sign > cheque.sign
```

Vérification du chèque par le vendeur et préparation du chèque pour le début
si ce dernier est valide :
```sh
python checkCheque.py < cheque.sign > cheque.seller.sign
```

Encaissement du chèque par le vendeur :
```sh
python deposit.py < cheque.seller.sign
```

Remarque :
Le format de signature utilisé n'offre pas de garantie contre l'inversion
de blocs de la signature. On pourrait ajouter un numéro en début de bloc
avant le chiffrement avec l'exposant privé. Comme cela, une fois le
déchiffrement avec l'exposant publique, on peut détecter les inversions et les
recoller dans l'ordre.

Pour sécurisé un plus la signature, on peut utiliser le mécanisme précédent
et mélanger les blocs obtenues lors de la réalisation du chiffrement avec
l'exposant privé.
