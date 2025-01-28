# boss.py

import random

class Boss:
    def __init__(self, name, hp, mana, attack, defense, special_ability=None):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.special_ability = special_ability  # Capacité spéciale du boss

    def use_special_ability(self, player):
        """Utilise la capacité spéciale du boss contre le joueur."""
        if self.special_ability == "Fury":
            damage = self.attack * 2
            player.take_damage(damage)
            return f"{self.name} utilise Fury et inflige {damage} dégâts!"
        elif self.special_ability == "Summon Minions":
            minion_count = random.randint(2, 5)
            return f"{self.name} invoque {minion_count} minions pour l'aider dans le combat!"
        elif self.special_ability == "Dark Heal":
            heal_amount = 200
            self.hp += heal_amount
            return f"{self.name} utilise Dark Heal et récupère {heal_amount} HP!"
        else:
            return f"{self.name} ne peut pas utiliser de capacité spéciale."

    def take_damage(self, damage):
        """Le boss peut prendre moins de dégâts que les ennemis standards."""
        reduced_damage = damage - self.defense
        self.hp -= max(reduced_damage, 0)  # Eviter de réduire la vie à un nombre négatif
        return self.hp
