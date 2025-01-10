import subprocess
import os
import time
import sys
from PIL import Image

# Fonction pour capturer une image depuis un flux
def capture_image_from_stream(stream_url, output_folder):
    """
    Capture une image unique depuis un flux en direct, avec une numérotation incrémentale.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recherche du dernier numéro utilisé pour les images
    existing_files = [f for f in os.listdir(output_folder) if f.endswith('.jpg') and f.startswith("frame_")]
    existing_numbers = [
        int(f.split('_')[1].split('.')[0]) for f in existing_files if f[6:9].isdigit()
    ]
    next_number = max(existing_numbers, default=0) + 1

    # Définir le nom du fichier suivant avec la numérotation
    output_pattern = os.path.join(output_folder, f"frame_{next_number:03d}.jpg")
    
    # Commande ffmpeg pour capturer une image
    command = [
        "ffmpeg", "-i", stream_url,
        "-vframes", "1",  # Capture une seule image
        output_pattern
    ]
    
    try:
        # Exécution de la commande sans afficher de sortie
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_pattern
    except subprocess.CalledProcessError:
        print("Erreur lors de l'exécution de la commande ffmpeg.")
    except FileNotFoundError:
        print("Erreur : ffmpeg n'est pas installé ou accessible.")
    return None

# Fonction pour obtenir des pixels "pseudo-aléatoires" à partir de l'heure et de la date
def obtenir_pixels_aleatoires(image_path, n=50):
    """
    Ouvre une image et retourne les n premières valeurs RGB des pixels,
    mais choisies de manière pseudo-aléatoire en fonction de l'heure et de la date.
    """
    try:
        image = Image.open(image_path)
        image_np = list(image.getdata())
        
        # Dimension de l'image
        largeur, hauteur = image.size
        taille_image = largeur * hauteur
        
        # Obtenir l'heure actuelle en secondes
        current_time = time.time()  # Temps en secondes depuis l'époque (timestamp Unix)
        
        # Utilisation de la partie fractionnaire du temps pour diversifier
        time_fraction = current_time - int(current_time)  # Partie fractionnaire du temps
        base_offset = int(time_fraction * 1000000)  # Multiplie pour augmenter la diversité
        
        # Calculer des indices pseudo-aléatoires basés sur l'heure et la date
        valeurs_rgb = []
        for i in range(n):
            # Calculer un indice unique basé sur le temps et un facteur de décalage
            index = (base_offset + i * 999) % taille_image  # Décalage pour éviter les pixels consécutifs
            valeurs_rgb.extend(image_np[index])  # Ajoute R, G, B séparément

        return valeurs_rgb[:n]
    
    except Exception as e:
        print(f"Erreur lors de l'ouverture ou du traitement de l'image : {e}")
    return None

# Fonction pour afficher un grand nombre formé par les valeurs RGB
def afficher_grand_nombre(valeurs_rgb, n=50):
    """
    Affiche un très grand nombre formé par les valeurs RGB, limité à n caractères.
    """
    # Créer un grand nombre en concaténant les valeurs RGB
    grand_nombre = ''.join(str(valeur) for valeur in valeurs_rgb)
    
    # Limiter le nombre à n caractères
    grand_nombre_limite = grand_nombre[:n]
    
    print(f"Voici les {n} caractères :")
    print(grand_nombre_limite)

# Exemple d'utilisation avec gestion d'argument en ligne de commande
def main():
    # Vérifier si l'argument pour le nombre de caractères est fourni
    if len(sys.argv) != 2:
        print("Erreur : Il faut spécifier un nombre d'éléments à afficher en argument (ex. 50).")
        sys.exit(1)
    
    try:
        # Lire l'argument du nombre de caractères à afficher
        nombre_caracteres = int(sys.argv[1])
    except ValueError:
        print("Erreur : L'argument doit être un nombre entier.")
        sys.exit(1)

    # URL du flux et du dossier de sortie
    stream_url = ""
    output_folder = ""
    
    # Capturer une image
    image_path = capture_image_from_stream(stream_url, output_folder)

    if image_path:
        # Obtenir les premières n valeurs RGB des pixels pseudo-aléatoires
        premieres_rgb = obtenir_pixels_aleatoires(image_path, nombre_caracteres)
        if premieres_rgb is not None:
            # Afficher les valeurs RGB comme un très grand nombre
            afficher_grand_nombre(premieres_rgb, nombre_caracteres)
        else:
            print("Impossible de récupérer les valeurs RGB.")
    else:
        print("Aucune image n'a été capturée.")

if __name__ == "__main__":
    main()