# pBdd
projet bdd 2021_2022 python

Pour lancer le programme, il faut lancer main.py

Au demarrage, le programme va vous demander de charger un fichier qui est une bdd (base de donné) qui se lit avec sqlite3 ( test.db est deja present), il faudra seulement ecrire le nom du fichier sans son extension ".db" ( exemple : pour utiliser la bdd test.db il faut juste ecrire "test"). Ensuite, de base la bdd n'a pas de DF ( dependance fonctionelle) donc vous pourrez soit creer des DF, soit charger une sauvegarde ( il y a une sauvegarde "tt.txt" qui est deja presente) sans son extension ".txt" ( exemple : pour charger tt.txt il faut juste ecrire "tt". Les sauvegardes et les bases de données doivent être dans le meme repertoire que main.py!

Le menu principal permet d'afficher les DF, de sauvegarder les DF, de charger une sauvegarde de DF et d'aller dans le menu concerant les DF.
Le menu concernant les DF permet d'afficher les DF, d'ajouter une DF, de modifier un DF, de supprimer une DF, de générer des clé a partir de DF, de vérifier que les normes BNCF et 3NF sont respectés (pour toutes les tables) ou de supprimer toutes les DF.

Lorsque vous voudrez creer un nouvelle DF, il faudra selectionner sur quelle table portera votre DF avec un numéro, il faudr ensuite introduire les elements qui seront a la gauche de la DF en les separant d'un espace (exemple : pour mettre les elements A, C et B à gauche d'une DF pour keyT, il faut ecrire "A C B"). Il est egalement possible de modifier une DF qui existe deja.

Lorsque vous afficher les DF, si il y a plus d'une DF, cela vous proposera également d'afficher celles qui ne sont pas satisfaitent ou celles étants des consequences. Lorsque vous afficher les clés d'une table, cela vous proposera d'afficher également si cette table respecte les normes 3NF et BCNF. 

Une erreur sera généré si vous chargez un mauvaise sauvegarde/une mauvaise bdd/une mauvaise table/ un mauvais argument.

La vérification d'une DF a des attributs présent dans une table est réalisé avant chaque operation agissant sur la bdd.
