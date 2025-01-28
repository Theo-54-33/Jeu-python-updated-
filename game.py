import pygame
import sys
from player import Player
from enemy import Enemy
from battle import Battle

def main():
    """Point d'entrée du jeu."""
    pygame.init()  # Initialisation de Pygame
    screen = pygame.display.set_mode((800, 600))  # Création de la fenêtre
    pygame.display.set_caption("Combat Game")  # Titre de la fenêtre

    # Créer un joueur
    player = Player(name="Noctis", hp=200, attack=30, defense=10, mana=100)

    # Démarrer le combat
    battle = Battle(screen, player)  # Passer uniquement screen et player
    battle.start()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
