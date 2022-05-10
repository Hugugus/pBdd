# pBdd
projet bdd 2021_2022 python


Au demarrage, le programme va vous demannder charger un fichier qui est une bdd (base de donné) qui se lit avec sqlite3 ( test.db est deja present), il faudra ecrire seulement ecrire le nom du fichier sans son extension ".db" ( exemple : pour utiliser la bdd test.db il faut juste ecrire "test"). Ensuite, de base la bdd n'a pas de DF ( dependance fonctionelle) donc vous pourrez soit creer des DF, soit charger une sauvegarde ( il y a une sauvegarde "tt.txt" deja presente) sans son extension ".txt" ( exemple : pour charger tt.txt il faut juste ecrire "tt".

Il est possible d'afficher une table entiere. Lorsque vous voudrez creer un nouvelle DF, il faudra selectionner sur quelle table portera votre DF avec un numéro, il faudr ensuite introduire les elements qui seront a la gauche de la DF en les separant d'un espace (exemple : pour mettre les elements A, C et B à gauche d'une DF pour keyT, il faut ecrire "A C B"). Il est egalement possible de modifier une DF qui existe deja.

Lorsque vous afficher les DF, si il y a plus d'une DF, cela vous proposera également d'afficher celles qui ne sont pas satisfaitent ou celles étants des consequences.

Il est possible d'afficher les clé d'une table et d'ensuite verifier si elle verifie les normes 3NF et BCNF. Il est aussi possible de modifier d'afficher tout cela pour toute les table de la bdd
