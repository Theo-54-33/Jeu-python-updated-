class Spell:
    def __init__(self, name, damage, mana_cost):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost

# Exemple de sorts
fireball = Spell("Fireball", 30, 10)
heal = Spell("Heal", -20, 15)
