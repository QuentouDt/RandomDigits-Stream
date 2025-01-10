# RandomDigits-Stream

RandomDigits-Stream est un script Python qui capture une image depuis un flux vidéo en direct, extrait des valeurs RGB "pseudo-aléatoires" de cette image, et les utilise pour afficher nombre. Ce projet combine des fonctionnalités liées à l'extraction d'images, au traitement d'images et à la manipulation de données pseudo-aléatoires.

# Fonctionnalités

Capture une image depuis un flux vidéo en direct en utilisant ffmpeg.

Génère des indices "pseudo-aléatoires" basés sur le temps pour sélectionner des pixels.

Affiche un nombre basé sur les valeurs RGB des pixels extraits.

# Prérequis

Python 3.x

ffmpeg : doit être installé et accessible via la ligne de commande.

Pillow : bibliothèque Python pour la manipulation d'images. Installation via :

# Installation

Clonez ce dépôt :

```bash
git clone https://github.com/votre_nom_utilisateur/StreamRandomPixelRGB.git
```

Exécutez le script en ligne de commande en spécifiant le nombre de caractères à afficher :

```bash
python script.py <nombre_de_caracteres>
```

Par défaut, l'image capturée sera enregistrée dans le dossier défini dans la variable output_folder. Vous pouvez modifier cette variable directement dans le script.

# Paramètres

stream_url : URL du flux vidéo. Remplacez l'URL par celle de votre choix dans le script.

output_folder : Dossier où les images capturées seront enregistrées.
