import pygame
import subprocess
import os
from enemy import Enemy
from player import Player  # Assurez-vous d'importer Player ici
from battle import Battle
from save import save_game, load_game

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 800, 600

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.button_click_sound = None
        self.main_theme = 'ressources/music/main_theme.mp3'
        
        try:
            pygame.mixer.music.load(self.main_theme)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Erreur de chargement de la musique principale : {e}")
        
        try:
            self.button_click_sound = pygame.mixer.Sound('ressources/sounds/button_click.mp3')
        except pygame.error as e:
            print(f"Erreur lors du chargement du son de clic : {e}")
            self.button_click_sound = None
        
        # Liste des boutons
        self.buttons = [
            {"text": "Nouvelle Partie", "action": self.new_game, "rect": pygame.Rect(300, 200, 200, 50)},
            {"text": "Charger Partie", "action": self.load_game, "rect": pygame.Rect(300, 270, 200, 50)},
            {"text": "Quitter", "action": self.quit_game, "rect": pygame.Rect(300, 340, 200, 50)},
        ]

    def new_game(self):
        """Démarre une nouvelle partie avec des données par défaut."""
        if self.button_click_sound:
            self.button_click_sound.play()

        self.stop_music()

        # Lancer l'écran de chargement avant de démarrer une nouvelle partie
        try:
            subprocess.run(["python3", "loading.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du lancement de loading.py : {e}")
            return

        # Créer un joueur avec des données par défaut
        player_data = Player(name="Noctis", hp=200, mana=100, attack=30, defense=50, level=1)
        
        # Créer un ennemi pour le combat
        enemy = Enemy(name="Goblin", hp=100, attack=20, defense=5)  # Exemple d'ennemi

        # Sauvegarder les données par défaut
        save_game(player_data)

        # Lancer le combat avec le joueur et l'ennemi
        self.start_battle(player_data, enemy)

    def load_game(self):
        """Charger une partie existante."""
        if self.button_click_sound:
            self.button_click_sound.play()

        self.stop_music()

        # Charger les données du joueur depuis le fichier de sauvegarde
        player_data = load_game()  # Vous devez implémenter la fonction load_game dans save.py

        if player_data is None:
            print("Aucune sauvegarde trouvée.")
            return

        # Créer un ennemi pour le combat (vous pouvez personnaliser cela selon l'état de la sauvegarde)
        enemy = Enemy(name="Goblin", hp=100, attack=20, defense=5)  # Exemple d'ennemi

        # Lancer le combat avec les données du joueur et de l'ennemi
        self.start_battle(player_data, enemy)

    def start_battle(self, player_data, enemy):
        """Lancer le combat avec les données du joueur et de l'ennemi."""
        battle = Battle(self.screen, player_data, enemy)  # Passer les deux objets ici
        battle.start()  # Utiliser la méthode start() pour démarrer le combat

    def stop_music(self):
        """Arrêter la musique en cours uniquement si elle joue.""" 
        if pygame.mixer.music.get_busy():  # Vérifie si la musique est en train de jouer
            pygame.mixer.music.stop()

    def quit_game(self):
        """Quitte le jeu."""
        pygame.quit()
        exit()

    def run(self):
        """La boucle principale du menu.""" 
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Fond noir

            # Afficher les boutons
            for button in self.buttons:
                pygame.draw.rect(self.screen, (0, 128, 255), button["rect"])
                text = self.font.render(button["text"], True, (255, 255, 255))
                self.screen.blit(text, (button["rect"].x + 20, button["rect"].y + 10))

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifier si un bouton a été cliqué
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()  # Appeler l'action associée au bouton

            pygame.display.flip()  # Mettre à jour l'écran

        pygame.quit()

def main():
    """Point d'entrée du programme."""
    pygame.init()  # Initialisation de Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Création de la fenêtre
    pygame.display.set_caption("Project")  # Titre de la fenêtre

    # Créer l'objet menu et démarrer le jeu
    menu = MainMenu(screen)
    menu.run()  # Démarrer la boucle du menu principal

if __name__ == "__main__":
    main()
