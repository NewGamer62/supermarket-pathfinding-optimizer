# README :

**Dans les dossiers correspondant :**

* Pour lire la première application, veuillez lancer "main.py", lire la notice d'utilisation et tester le projet "Sauvegarde-Test" en ouvrant directement dans l'application.
* Pour la deuxième application, veuillez lancer "mainApp2.py".

**Remarque :** Certaines actions en particulier risquent de ne pas fonctionner ou même provoquer un plantage. Veuillez nous excuser pour la gêne occasionnée.

---

# Ajouts possibles :

Au cours de ce projet, nous n'avons pas eu le temps de travailler sur toutes nos idées. Cependant voici nos idées afin d'améliorer ce projet :

* Créer un système de référencement des produits. Cela serait utile notamment pour optimiser les données dans les fichiers.
* Un algorithme permettant de placer des murs, des caisses et des entrées automatiquement sur la plan. On peut l'implémenter en supposant que si une case est remplie à 60% alors c'est un mur ou une caisse, que là où les clients rentrent soit une entrée etc...
* La possibilité d'importer automatiquement le dernier projet en date,de la 1ère application, au démarrage de la 2e application. Uniquement pour rendre plus fluide l'utilisation des applications. En effet devoir tout le temps ouvrir les fichier pour importer un plan ce n'est pas ergonomique. D'autant que souvent, après la création d'un projet depuis l'application 1, il est probable que le client utilise l'application 2 pour utiliser son projet.

---

# Auteurs :

* Louis AMEDRO, TPD (responsable) (Osiris Sio)
* Jules HERBAUX, TPD (Lirei159)
* Valentin MINNEBO, TPA (Jonedeuf)
* Noa GAILLARD, TPC (NewGamer62)

![](annexes/logo_APM.png)
***Réalisé par APP MAKER.***

---

# Journal de bord :

### Mardi 10 Juin : 8h30 à 11h30 et 13h00 à 17h30 (en présentiel)

* **Louis :** J'ai organiser le groupe (leader) et répartit certaines tâche sur Trello et créer certaines branches. J'ai réalisé la vue du plan pour le magasin (zoom, grille, ajustement,...)
* **Jules :** Réalisation Logo d'équipe, de la charte graphique des vue (optionnelle) et le futur design des éléments des vues (plan_vue.png)
* **Noa :** Aujourd'hui j'ai fait le figma pour avoir l'idée générale de l'application avec Jules (plan_vue.png). Ensuite j'ai commencé à faire l'application n°1 en commençant par la partie supérieure droite (informations) et j'ai ainsi découpé les vues pour faciliter le travail en équipe sur les vues (exemple, avec Louis)
* **Valentin :** Je me suis chargé de la conception du modèle commun aux deux applications. J'ai d'abord réalisé un schéma représentant toutes les classes nécessaires à la réalisation du modèle ainsi que leurs attributs et leurs méthodes (dans plan_modele.pdf). Puis j'ai discuté avec mes camarades pour déterminer les éléments à laisser et à garder dans les modèles. Enfin, j'ai développé de A à Z la classe Informations qui fera partie du modèle final, et cela en comprenant les commentaires, docstrings et les tests unitaires.

### Mercredi 11 Juin : 8h30 à 11h30 et 13h00 à 17h30 (en présentiel)

* **Louis :** J'ai toujours recadrer l'équipe. J'ai fini le premier prototype du plan (dont, le imageZoomable.py), c'est à dire l'ajout d'une matrice, convertie à ce qu'on a dans la grille de Qt et qui sera donner au contrôleur, puis au modèle. Il manque encore des petits réglages mais ça sera fait sûrement demain en faisant une première fusion/teste de l'application.
* **Jules :** Matin, examen Cisco. Après midi, j'ai terminé le texte design_elements qui contient toutes les modifications graphiques à apporter à la vue. J'ai commencé et presque terminé le dossier Clair.qss, il permet de styliser la vue de la 1ère application en mode clair.
* **Noa :** Aujourd'hui j'ai fais les parties de vues pour la liste des produits par case, fini celle des informations, fait le bandeau et les boutons pour placer les éléments sur le plan.
* **Valentin :** J'ai continué la conception du modèle de l'application. Ayant précédemment fini la classe Informations, j'ai développé la classe Supermarché qui fera également partie du modèle final. La majorité des méthodes concernant la première application ont été développées, et cela en comptant les commentaires docstrings. Il ne reste plus qu'à développer les méthodes pour la deuxième application, les tests pour la classe Supermarché et le modèle final rassemblant Informations et Supermarché.

### Jeudi 12 Juin : 8h30 à 11h30 et 13h00 à 17h30 (en présentiel, sauf Jules = malade, donc télétravail)

* **Louis :** J'ai récupérer tous les fichiers de chaque branches pour le mettre dans le Dev pour les fusionner et faire les premiers essais. J'ai relier tout ça avec la vue.py et le controleur.py et régler les premiers bugs avec l'aide de Noa et de Valentin. Les vues sont bonnes entre eux mais le controleur à encore du mal. J'ai fini pas remettre à jour les branches vue, ui, modéle et controleur avec tous les fichiers nécessaires pour les testes.
* **Jules :** Malade (fièvre) donc télétravail imposé. J'ai terminé le qss de la 1ère application (en mode clair et sombre). J'ai également fait un schéma de l'état de nos branches après avoir tout fusionné avec dev. Et pour finir j'ai rédigé la notice d'utilisation de la 1ère application (encore à modifier).
* **Noa :** Aujourd'hui j'ai réalisé le figma de l'appli, fais/commencé la vue de l'application 2 ainsi que la vueListeProduit, j'ai harmonisé l'ensemble des vues déjà existante (lowerCamelCase, nom de variable, commentaire) et assisté Louis dans le débogage de l'appli 1
* **Valentin :** J'ai encore continué le modèle de l'application. Toute les méthodes de l'application 1 sont finies et j'ai développé la majorité des méthodes concernant l'application 2. J'ai également codé l'ébauche du modèle final utilisé dans l'application. Il me faut encore développer quelques méthodes, rajouter des docstrings, coder le main pour tester la classe supermarché puis créer les docstrings/tests pour le modèle final.

### Vendredi 13 Juin : 8h30 à 11h30 et 13h00 à 19h00 (en présentiel, puis télétravail selon les derniers commits)

* **Louis :** J'ai fini la partie UI (User Interface) avec Jules mais nous avons eu un petit problème avec la police Nunito. On a donc dû repassé dessus. J'ai corriger tous les derniers problèmes de la première application (spoiler, il y en a encore). J'ai réorganiser les dossiers et fusionner tout dans la branche main. J'ai fini en écrivant les derniers petits choses du README.
* **Jules :** (Parti à 17h30, télétravail) Aujourd'hui j'ai finalisé la partie design (qss) à l'aide de Louis, nous avons essayé d'implémenter une police spécifique sans succès et nous sommes donc revenus à la base. J'ai terminé la notice avec l'application 1 finalisée avec le design. J'ai importé notre journal de bord de la semaine dans notre README.
* **Noa :** (Parti à 18h) Aujourd'hui j'ai lié la vue et le modèle grace au controapp2 et établi un mainapp2, en adaptant les fichiers quand nécessaire
* **Valentin :** J'ai fini le modèle de l'application. Toutes les méthodes sont finies, ainsi que les commentaires docstrings qui les accompagnent. Les seules choses qui manquent sont les tests dans le main.
