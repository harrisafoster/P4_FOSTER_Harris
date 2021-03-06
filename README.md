# P4_FOSTER_Harris
Gestionnaire des tournois d'échecs

Projet 4 OpenClassrooms

Ce gestionnaire de tournois multifonction d'échecs peut : 

1. Gérer tous vos tournois d'échecs de début à la fin
2. Sauvegarder toutes les données nécessaires en rapport avec vos tournois/joueurs 
3. Générer des rapports sur tous vos tournois et joueurs

## Installation
### Pour les développeurs et utilisateurs (windows 10, mac, linux) :
#### Clonez la source localement (en utilisant Git Bash) :
```sh
$ git clone https://github.com/harrisafoster/P4_FOSTER_Harris
$ cd P4_Foster_Harris
```
#### Créer et activer un environnement virtuel avec (windows 10) :
```sh
$ python -m venv env
$ source ./env/Scripts/activate
```
#### Créer et activer un environnement virtuel avec (mac & linux) :
```sh
$ virtualenv venv
$ source venv/bin/activate
```
#### Et installez les packages requis avec :
```sh
$ pip install -r requirements.txt
```

## Peluchage du code avec flake8
#### Vous pouvez vérifier qu'il n'y à aucun problème du style PEP8 avec les commandes suivantes :
#### Générer un rapport flake8 sur les fichiers nécessaires avec : 
```sh
$ flake8 --max-line-length 119 controllers.py views.py tournament_manager.py models\ --format=html --htmldir=flake-report
```
#### Lire le rapport avec :
```sh
$ cat flake-report/index.html
```
#### Ou vous pouvez simplement ouvrir le fichier index.html dans votre navigateur avec :
```sh
$ open -a "nom_de_votre_navigateur" flake-report/index.html
```


## Utilisation
### Puis vous pouvez exécuter le logiciel depuis votre terminal avec :
```sh
$ python tournament_manager.py
```

Dès que le logiciel est lancé, vous pouvez naviguer les menus principaux 
pour effecteur vos tournois et rapports à l'aide de votre clavier. 

Quand vous commencez un tournoi, sa date de début est renseignée automatiquement par le logiciel et la 
même chose se passe quand vous terminez un tournoi avec sa date de fin. Similairement, quand vous confirmez 
que vous commencez un tour (round), sa date et heure de début sont sauvegardées automatiquement. Quant à la 
fin de chaque tour, la date et heures sont automatiquement sauvegardées selon la durée que vous renseignez à la 
fin de chaque tour. Il est donc impératif de confirmer le début d'un tour au moment où il commence et de renseigner 
une durée exacte. 

Il est utile de préciser que vous pouvez sauvegarder votre progrès et modifier les classements des joueurs 
dans la base de données à la fin de chaque tour ou à la fin de chaque match. Il suffit de sauvegarder votre progrès quand 
le logiciel vous demande si vous voulez continuer, et puis naviguer dans le menu edit/add_players pour 
effectuer les changements de classement.

Pour montrer les résultats d'un tournoi, il suffit d'aller dans les menus des "local reports" et spécifier quel rapport
vous souhaitez montrer. 

## Built with
Python 3.9