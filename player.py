class Player:
    def __init__(self, name, hp, attack, defense, mana, level=1):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.level = level
        self.is_alive = True

    def take_damage(self, damage):
        if damage < 0:
            damage = 0
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
        return self.hp

    def heal(self, amount):
        if self.hp <= 0:
            return  # Ne pas soigner si le joueur est mort
        self.hp += amount
        return self.hp

    def attack_enemy(self, enemy):
        if not self.is_alive:
            return 0  # Le joueur ne peut pas attaquer s'il est mort
        damage = max(0, self.attack - enemy.defense)
        enemy.take_damage(damage)
        return damage

    def is_dead(self):
        return not self.is_alive
