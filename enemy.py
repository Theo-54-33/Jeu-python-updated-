class Enemy:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def attack_player(self, player):
        """Effectue une attaque sur le joueur."""
        damage = max(self.attack - player.defense, 0)
        player.take_damage(damage)
        return damage

    def take_damage(self, damage):
        """Applique des dégâts à l'ennemi."""
        self.hp -= damage

    def is_alive(self):
        """Vérifie si l'ennemi est encore en vie."""
        return self.hp > 0

class Boss(Enemy):
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)
        # Vous pouvez ajouter des caractéristiques spécifiques au boss ici
        self.is_boss = True  # Indiquer que c'est un boss

class FinalBoss(Boss):
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)
        # Vous pouvez ajouter des caractéristiques spécifiques au boss final ici
        self.is_final_boss = True  # Indiquer que c'est un boss final
