# final_boss.py

from boss import Boss  # Importer Boss depuis boss.py

class FinalBoss(Boss):
    def __init__(self, name="Final Boss", hp=1000, mana=500, attack=200, defense=150, special_ability="Ultime Attack"):
        # Appeler le constructeur parent (Boss)
        super().__init__(name, hp, mana, attack, defense, special_ability)

    def use_special_ability(self, player):
        """Capacité spéciale pour le boss final : Ultimate Destruction."""
        if self.special_ability == "Ultimate Destruction":
            damage = self.attack * 3
            player.take_damage(damage)
            return f"{self.name} utilise Ultimate Destruction et inflige {damage} dégâts dévastateurs!"
        else:
            return super().use_special_ability(player)  # Appeler la méthode parent si aucune capacité spéciale
