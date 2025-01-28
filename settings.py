import pygame
import sys
import os
import subprocess
import json  # Pour sauvegarder les paramètres
from pygame.locals import *
from save import save_game, load_game, reset_save
from data import PlayerData
from battle import Battle

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 800, 600

# Définir le dossier de sauvegarde
SAVE_FOLDER = "saves"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Paramètres par défaut
DEFAULT_SETTINGS = {
    "music_volume": 1.0,  # Volume musique (0.0 à 1.0)
    "sfx_volume": 1.0,  # Volume effets sonores (0.0 à 1.0)
    "resolution": (800, 600),  # Résolution par défaut
    "fullscreen": False  # Mode plein écran
}

class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self.load_settings()

    def load_settings(self):
        """Charge les paramètres à partir du fichier JSON."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = DEFAULT_SETTINGS
            self.save_settings()

    def save_settings(self):
        """Sauvegarde les paramètres dans le fichier JSON."""
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def set_music_volume(self, volume):
        """Modifie le volume de la musique."""
        self.settings["music_volume"] = volume
        pygame.mixer.music.set_volume(volume)
        self.save_settings()

    def set_sfx_volume(self, volume):
        """Modifie le volume des effets sonores."""
        self.settings["sfx_volume"] = volume
        self.save_settings()

    def set_resolution(self, resolution):
        """Modifie la résolution de la fenêtre."""
        self.settings["resolution"] = resolution
        pygame.display.set_mode(resolution)
        self.save_settings()

    def toggle_fullscreen(self):
        """Passe du mode fenêtré au mode plein écran et inversement."""
        self.settings["fullscreen"] = not self.settings["fullscreen"]
        if self.settings["fullscreen"]:
            pygame.display.set_mode(self.settings["resolution"], pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(self.settings["resolution"])
        self.save_settings()

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        self.button_click_sound = None
        self.main_theme = 'ressources/music/main_theme.mp3'

        # Musique de fond du menu principal
        try:
            pygame.mixer.music.load(self.main_theme)
            pygame.mixer.music.play(loops=-1)
        except pygame.error:
            print("Erreur de chargement de la musique principale.")
        
        # Son de clic pour les boutons
        try:
            self.button_click_sound = pygame.mixer.Sound('ressources/sounds/button_click.mp3')
        except pygame.error:
            print("Erreur lors du chargement du son de clic.")
            self.button_click_sound = None  # Si le son échoue, on l'ignore
        
        # Définition des boutons du menu principal
        self.buttons = [
            {"text": "Nouvelle Partie", "action": self.new_game},
            {"text": "Charger Partie", "action": self.load_game},
            {"text": "Options", "action": self.open_options},
            {"text": "Quitter", "action": self.quit_game},
        ]
        self.selected_button = 0  # Index du bouton sélectionné
        self.settings = Settings()  # Paramètres

    def stop_music(self):
        """Arrête la musique en cours."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def render_button(self, text, y_pos, is_selected=False):
        """Affiche un bouton sur l'écran avec un effet de survol."""
        color = (255, 255, 255) if not is_selected else (255, 0, 0)
        label = self.font.render(text, True, color)
        rect = label.get_rect(center=(WIDTH // 2, y_pos))
        
        if is_selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(20, 10), 2)
        self.screen.blit(label, rect)
        return rect

    def new_game(self):
        """Démarre une nouvelle partie avec des données par défaut."""
        if self.button_click_sound:
            self.button_click_sound.play()

        # Arrêter la musique du menu avant de lancer loading.py
        self.stop_music()

        # Lancer l'écran de chargement avant de démarrer une nouvelle partie
        subprocess.run(["python", "loading.py"])

        # Créer un joueur avec des données par défaut
        player_data = PlayerData(name="Noctis", hp=100, mana=50, attack=10, defense=5, level=1)
        save_game(player_data)
        
        # Lancer le jeu (ici, lancer un combat)
        self.start_battle(player_data)

    def load_game(self):
        """Charge une partie sauvegardée."""
        if self.button_click_sound:
            self.button_click_sound.play()

        # Arrêter la musique du menu avant de lancer loading.py
        self.stop_music()

        subprocess.run(["python", "loading.py"])

        save_files = self.get_save_files()
        if save_files:
            save_name = save_files[0]
            player_data = load_game(save_name)
            
            if player_data:
                print(f"Partie chargée : {player_data.name}, Niveau {player_data.level}")
                self.start_battle(player_data)
            else:
                self.show_message("Erreur lors du chargement de la partie.", title="Erreur")
        else:
            self.show_message("Aucune sauvegarde disponible.", title="Erreur")

    def open_options(self):
        """Ouvre l'écran des options."""
        options_menu = OptionsMenu(self.screen, self.settings)
        options_menu.run()

    def quit_game(self):
        """Quitte le jeu."""
        if self.button_click_sound:
            self.button_click_sound.play()
        pygame.quit()
        sys.exit()

    def get_save_files(self):
        """Retourne la liste des fichiers de sauvegarde dans le répertoire spécifié."""
        return [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".save")]

    def show_message(self, message, title="Message"):
        """Affiche un message à l'écran."""
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Remplir l'écran avec une couleur noire
            self.screen.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Appuie sur Entrée pour fermer
                        running = False

    def start_battle(self, player_data):
        """Lancer le combat avec les données du joueur."""
        battle = Battle(self.screen, player_data)
        battle.start_battle()

    def handle_input(self):
        """Gérer l'entrée clavier et la navigation entre les boutons."""
        keys = pygame.key.get_pressed()
        
        if keys[K_UP]:
            self.selected_button = (self.selected_button - 1) % len(self.buttons)
        elif keys[K_DOWN]:
            self.selected_button = (self.selected_button + 1) % len(self.buttons)
        
        if keys[K_RETURN]:  # Entrée pour sélectionner un bouton
            self.buttons[self.selected_button]["action"]()

    def run(self):
        """Lance le menu principal et gère les événements."""
        running = True
        y_pos = 200
        button_rects = []
        
        while running:
            self.screen.fill((0, 0, 0))  # Remplir l'écran avec une couleur noire
            
            self.handle_input()  # Gérer l'entrée clavier pour la navigation

            # Affichage du titre
            title_label = self.title_font.render("Final Fantasy Beta", True, (255, 215, 0))
            title_rect = title_label.get_rect(center=(WIDTH // 2, 100))
            self.screen.blit(title_label, title_rect)
            
            button_rects.clear()
            for i, button in enumerate(self.buttons):
                is_selected = i == self.selected_button
                button_rect = self.render_button(button["text"], y_pos + i * 60, is_selected)
                button_rects.append(button_rect)

            pygame.display.update()
            pygame.time.Clock().tick(60)  # Limiter à 60 images par seconde


class OptionsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.Font(None, 48)
        self.selected_option = 0  # Option sélectionnée par défaut

    def render_option(self, text, y_pos, is_selected=False):
        """Affiche une option avec un effet de survol."""
        color = (255, 255, 255) if not is_selected else (255, 0, 0)
        label = self.font.render(text, True, color)
        rect = label.get_rect(center=(WIDTH // 2, y_pos))
        
        if is_selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(20, 10), 2)
        self.screen.blit(label, rect)
        return rect

    def handle_input(self):
        """Gère les touches pour naviguer dans le menu des options."""
        keys = pygame.key.get_pressed()
        
        if keys[K_UP]:
            self.selected_option = (self.selected_option - 1) % 4
        elif keys[K_DOWN]:
            self.selected_option = (self.selected_option + 1) % 4
        
        if keys[K_RETURN]:  # Entrée pour valider une option
            self.apply_option()

    def apply_option(self):
        """Applique l'option sélectionnée."""
        if self.selected_option == 0:
            # Ajuster le volume de la musique
            volume = self.settings.settings["music_volume"]
            volume = (volume + 0.1) % 1.1  # Incrémenter de 0.1 et revenir à 0 si > 1
            self.settings.set_music_volume(volume)
        elif self.selected_option == 1:
            # Ajuster le volume des effets sonores
            sfx_volume = self.settings.settings["sfx_volume"]
            sfx_volume = (sfx_volume + 0.1) % 1.1
            self.settings.set_sfx_volume(sfx_volume)
        elif self.selected_option == 2:
            # Changer la résolution
            resolution = (1280, 720) if self.settings.settings["resolution"] == (800, 600) else (800, 600)
            self.settings.set_resolution(resolution)
        elif self.selected_option == 3:
            # Basculer plein écran
            self.settings.toggle_fullscreen()

    def run(self):
        """Lance le menu des options."""
        running = True
        y_pos = 200
        
        while running:
            self.screen.fill((0, 0, 0))  # Remplir l'écran avec une couleur noire
            self.handle_input()  # Gérer l'entrée clavier pour la navigation
            
            # Affichage du titre
            title_label = self.font.render("Options", True, (255, 215, 0))
            title_rect = title_label.get_rect(center=(WIDTH // 2, 100))
            self.screen.blit(title_label, title_rect)
            
            # Affichage des options
            options = [
                f"Musique: {int(self.settings.settings['music_volume'] * 100)}%",
                f"SFX: {int(self.settings.settings['sfx_volume'] * 100)}%",
                f"Résolution: {self.settings.settings['resolution'][0]}x{self.settings.settings['resolution'][1]}",
                "Plein écran: Oui" if self.settings.settings['fullscreen'] else "Plein écran: Non"
            ]
            
            for i, option in enumerate(options):
                is_selected = i == self.selected_option
                self.render_option(option, y_pos + i * 60, is_selected)

            pygame.display.update()
            pygame.time.Clock().tick(60)
