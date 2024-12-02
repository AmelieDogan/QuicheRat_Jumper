# QuicheRat_Jumper

Incarnez un petit rat en quête de délicieuses quiches ! Faites attention aux chartes médiévales qui pourraient vous être fatales... En cas de fatigue, le café Caron vous donnera la force de sauter.

## Installation

Créez un environnement virtuel pour le jeu : 

Dans votre terminal, allez à l’emplacement souhaité avec *cd* pour créer votre environnement virtuel puis tapez : 

```bash
	python3 -m venv jeux_python
```

Un dossier jeux_python va être créé

Pour l’activer : 

```bash
	source jeux_python/bin/activate
```

Pour pouvoir jouer, installez pygame dans l’environnement virtuel : 

```bash
	pip3 install pygame
```

Récupez l’ensemble des fichiers dans un dossier. Si votre environnement virtuel jeux_python est activé, alors il vous suffit d’aller avec *cd* dans votre dossier où se trouve le jeu et écrire : 

```bash
	python3 QuicheRat_jumper.py
```

Le jeu se lance !


## Description des commandes

Mangez un maximum de quiches en atteignant les plateformes sur lesquelles sont posées ces mets délicieux grâce aux commandes suivantes :

← (flèches de gauche) : se déplacer à gauche.

→ (flèches de droite) : se déplacer à droite.

Barre d'espace pour faire une double saut (rechargement des doubles sauts en attrapant des gobelets de café Caron).

Barre d'espace pour faire une nouvelle partie.

**Attention aux chartes médiévales qui vous seront fatales !**
