import pygame

def stop_music():
    """Arrêter la musique en cours."""
    pygame.mixer.music.stop()

def play_main_menu_music():
    """Jouer la musique du menu principal."""
    try:
        pygame.mixer.music.load('ressources/music/main_theme.mp3')
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        print("Erreur de chargement de la musique du menu principal")
