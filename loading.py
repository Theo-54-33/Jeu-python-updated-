import pygame
import sys
import time
from pygame.locals import *

# Initialisation de Pygame
pygame.init()

# Initialisation du mixeur pour le son
try:
    pygame.mixer.init()
except pygame.error:
    print("Erreur d'initialisation du module mixeur.")

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chargement")

# Charger la police pour afficher le texte
font = pygame.font.Font(None, 36)

def load_game():
    """Simule une barre de chargement de 20 secondes."""
    loading_start_time = time.time()  # Temps de début du chargement
    loading_duration = 20  # Durée de chargement en secondes

    running = True
    while running:
        screen.fill((0, 0, 0))  # Remplir l'écran avec une couleur noire

        # Calculer le pourcentage du chargement
        elapsed_time = time.time() - loading_start_time
        loading_percentage = min(100, (elapsed_time / loading_duration) * 100)

        # Dessiner une barre de chargement
        loading_bar_width = 600
        loading_bar_height = 30
        filled_width = int((loading_percentage / 100) * loading_bar_width)

        pygame.draw.rect(screen, (255, 255, 255), (100, HEIGHT // 2 - 20, loading_bar_width, loading_bar_height), 2)  # Bordure de la barre
        pygame.draw.rect(screen, (0, 255, 0), (100, HEIGHT // 2 - 20, filled_width, loading_bar_height))  # Partie remplie de la barre

        # Afficher le texte du pourcentage
        loading_text = font.render(f"Chargement: {int(loading_percentage)}%", True, (255, 255, 255))
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 + 40))

        # Vérifier si le temps est écoulé
        if elapsed_time >= loading_duration:
            # Après 20 secondes, quitter la boucle de chargement et lancer le jeu
            running = False
            start_game()

        # Vérifier les événements (permettre de fermer l'application si nécessaire)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        pygame.time.Clock().tick(60)  # Limiter à 60 images par seconde

def start_game():
    """Démarre le jeu après le chargement."""
    import game  # Importer et démarrer game.py
    game.main()

# Lancer la fonction de chargement
load_game()
