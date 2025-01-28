import json
import os
from data import PlayerData

SAVE_FOLDER = "saves"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def save_game(player_data, save_name="save1.save"):
    """Sauvegarde les données du joueur dans un fichier JSON."""
    try:
        save_path = os.path.join(SAVE_FOLDER, save_name)
        with open(save_path, 'w') as file:
            json.dump(player_data.to_dict(), file, indent=4)
        print("Sauvegarde réussie !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def load_game(save_name="save1.save"):
    """Charge les données du joueur depuis un fichier JSON."""
    save_path = os.path.join(SAVE_FOLDER, save_name)
    if os.path.exists(save_path):
        try:
            with open(save_path, 'r') as file:
                data = json.load(file)
            return PlayerData.from_dict(data)  # Retourne un objet PlayerData
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return None
    else:
        print("Aucune sauvegarde trouvée.")
        return None

def reset_save(save_name="save1.save"):
    """Réinitialise la sauvegarde (supprime le fichier)."""
    save_path = os.path.join(SAVE_FOLDER, save_name)
    if os.path.exists(save_path):
        os.remove(save_path)
        print("Sauvegarde réinitialisée.")
