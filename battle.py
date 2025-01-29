import pygame
import random
import time
from player import Player
from enemy import Enemy, Boss, FinalBoss
import subprocess

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 800, 600

class Battle:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.enemy = None
        self.font = pygame.font.Font(None, 36)
        self.actions = ["Attaquer", "Soigner", "Passer le Tour", "Quitter"]
        self.turn = "player"
        self.wave = 1

        # Initialiser pygame mixer pour jouer la musique
        pygame.mixer.init()

        # Liste des musiques de combat
        self.battle_music_files = [
            'ressources/music/battle_music.mp3',
            'ressources/music/battle_music2.mp3',
            'ressources/music/battle_music3.mp3',
            'ressources/music/battle_music4.mp3',
        ]
        # Musique pour les boss et final boss
        self.boss_music = 'ressources/music/boss_theme.mp3'
        self.final_boss_music = 'ressources/music/final_boss_theme.mp3'

    def play_random_battle_music(self):
        """Jouer une musique de combat aléatoire."""
        # Choisir une musique aléatoire ou une musique de boss
        if isinstance(self.enemy, (Boss, FinalBoss)):
            # Si le joueur affronte un boss ou final boss, jouer la musique spécifique
            music = self.boss_music if isinstance(self.enemy, Boss) else self.final_boss_music
        else:
            # Choisir une musique de combat régulière
            music = random.choice(self.battle_music_files)

        try:
            pygame.mixer.music.load(music)  # Charger la musique
            pygame.mixer.music.play(-1)  # Jouer en boucle (paramètre -1 pour boucle infinie)
            print(f"Musique en cours : {music}")  # Pour vérifier si la musique est correctement chargée
        except pygame.error as e:
            print(f"Erreur de chargement de la musique : {e}")

    def stop_battle_music(self):
        """Arrêter la musique de combat."""
        pygame.mixer.music.stop()

    def display_battle_info(self):
        """Affiche les informations du combat (HP du joueur et de l'ennemi)."""
        player_info = self.font.render(f"{self.player.name} - HP: {self.player.hp} Mana: {self.player.mana}", True, (255, 255, 255))
        enemy_info = self.font.render(f"{self.enemy.name} - HP: {self.enemy.hp}", True, (255, 0, 0))
        self.screen.blit(player_info, (10, 10))
        self.screen.blit(enemy_info, (10, 50))

    def display_turn_info(self):
        """Affiche le tour actuel du joueur ou de l'ennemi."""        
        turn_info = self.font.render(f"Tour de: {self.turn.capitalize()}", True, (255, 255, 255))
        self.screen.blit(turn_info, (WIDTH // 2 - 100, HEIGHT - 50))

    def display_actions(self):
        """Affiche les actions disponibles pendant le combat."""
        y_pos = 100
        for idx, action in enumerate(self.actions):
            action_text = self.font.render(f"{idx + 1}. {action}", True, (255, 255, 255))
            self.screen.blit(action_text, (10, y_pos))
            y_pos += 40

    def player_turn(self):
        """Gestion du tour du joueur."""
        damage = 0  # Initialiser damage ici pour qu'il soit toujours défini
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Attaquer
                    if not self.player.is_dead():
                        damage = self.player.attack_enemy(self.enemy)
                elif event.key == pygame.K_2:  # Soigner
                    if not self.player.is_dead():
                        self.player.heal(20)  # Soigner le joueur de 20 HP
                        damage = 0  # Soigner ne provoque pas de dégâts
                elif event.key == pygame.K_3:  # Passer le tour
                    damage = 0  # Aucun dégât quand on passe son tour
                elif event.key == pygame.K_4:  # Quitter
                    return False

                # Vérifier si damage a été modifié avant de l'utiliser
                if damage > 0:
                    self.enemy.take_damage(damage)
                    self.turn = "enemy"  # Le tour passe à l'ennemi après une action
                elif damage == 0 and event.key == pygame.K_3:
                    self.turn = "enemy"  # Si le joueur passe son tour, on passe directement à l'ennemi

        return True

    def enemy_turn(self):
        """Gestion du tour de l'ennemi."""
        if not self.enemy.is_alive():  # L'ennemi est mort, il ne peut pas attaquer
            return False
        if self.turn == "enemy" and self.player.hp > 0:  # L'ennemi n'attaque que si le joueur a agi
            action = random.choice(["attacker", "pass_turn"])
            if action == "attacker":
                damage = self.enemy.attack_player(self.player)
                self.turn = "player"  # Le tour passe au joueur après l'attaque de l'ennemi
            else:
                self.turn = "player"  # L'ennemi passe son tour sans attaquer
        return True

    def spawn_enemy(self):
        """Génère l'ennemi de la vague en fonction de la vague actuelle."""
        if self.wave < 10:
            self.enemy = Enemy(name="Goblin (lvl 1)", hp=100, attack=20, defense=5)  # Ennemi régulier
        elif self.wave == 10:
            self.enemy = Boss(name="Daemon (BOSS)(lvl ???)", hp=500, attack=50, defense=10)  # Boss
        elif self.wave == 11:
            self.enemy = FinalBoss(name="Ardyn Lucis Caelum (FINAL BOSS)(lvl ???)", hp=1000, attack=100, defense=50)  # Boss final

    def run_battle(self):
        """Démarre le combat avec les tours alternés et les vagues."""
        running = True
        self.play_random_battle_music()  # Jouer la musique de combat aléatoire au début du combat

        while running:
            self.screen.fill((0, 0, 0))
            self.display_battle_info()
            self.display_turn_info()
            self.display_actions()

            if self.turn == "player":
                # Le joueur choisit son action pendant son tour
                if not self.player_turn():
                    running = False
                    break
            elif self.turn == "enemy":
                # L'ennemi choisit son action pendant son tour
                if not self.enemy_turn():
                    running = False
                    break

            # Vérifier les conditions de fin de combat
            if self.player.is_dead():
                self.display_game_over()
                self.stop_battle_music()  # Arrêter la musique à la fin du combat
                running = False
                break
            elif self.enemy.is_alive() == False:  # Vérification avec la méthode is_alive()
                self.display_victory()
                self.wave += 1  # Passer à la prochaine vague

                if self.wave > 6:  # Fin du jeu après la dernière vague
                    self.display_game_over(final=True)
                    self.stop_battle_music()  # Arrêter la musique
                    running = False
                    break
                else:
                    self.spawn_enemy()  # Générer un nouvel ennemi pour la prochaine vague
                    self.turn = "player"  # Le joueur commence le nouveau combat
                    self.play_random_battle_music()  # Jouer la musique de la nouvelle vague

            pygame.display.update()
            pygame.time.Clock().tick(60)  # Limiter à 60 FPS

    def start(self):
        """Commencer le combat avec la première vague."""
        self.spawn_enemy()  # Générer l'ennemi de la première vague
        self.run_battle()

    def display_victory(self):
        """Affiche le message de victoire pour chaque vague."""
        victory_text = self.font.render("Vous avez gagné cette vague !", True, (0, 255, 0))
        self.screen.blit(victory_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.update()

        # Jouer le son de victoire
        try:
            pygame.mixer.music.load('ressources/sounds/victory.mp3')
            pygame.mixer.music.play()
            # Utiliser time.sleep pour attendre la fin de la musique, en calculant la durée approximative
            victory_music_duration = pygame.mixer.Sound('ressources/sounds/victory.mp3').get_length()
            time.sleep(victory_music_duration)  # Attendre la fin de la musique
        except pygame.error as e:
            print(f"Erreur de chargement du son de victoire : {e}")

    def display_game_over(self, final=False):
        """Affiche le message de game over."""
        if final:
            game_over_text = self.font.render("Vous avez vaincu le Boss Final !", True, (255, 0, 0))
        else:
            game_over_text = self.font.render("Vous êtes mort !", True, (255, 0, 0))
        self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Attendre avant de quitter
