# data.py

class PlayerData:
    def __init__(self, name, hp, mana, attack, defense, level, xp=0, enemies_defeated=0):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.level = level
        self.xp = xp  # Assurez-vous d'initialiser l'attribut xp
        self.enemies_defeated = enemies_defeated

    def to_dict(self):
        """Convertit l'objet PlayerData en dictionnaire."""
        return {
            "name": self.name,
            "hp": self.hp,
            "mana": self.mana,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "xp": self.xp,
            "enemies_defeated": self.enemies_defeated
        }

    @classmethod
    def from_dict(cls, data):
        """Crée un objet PlayerData à partir d'un dictionnaire."""
        return cls(
            name=data["name"],
            hp=data["hp"],
            mana=data["mana"],
            attack=data["attack"],
            defense=data["defense"],
            level=data["level"],
            xp=data.get("xp", 0),  # Utilisation de get pour xp, par défaut 0
            enemies_defeated=data.get("enemies_defeated", 0)  # Pareil pour enemies_defeated
        )

    def defeat_enemy(self):
        """Incrémente le compteur d'ennemis vaincus."""
        self.enemies_defeated += 1

    def gain_xp(self, xp):
        """Ajoute de l'expérience au joueur."""
        self.xp += xp
        if self.xp >= 100:  # Exemple : atteindre 100 XP permet de monter d'un niveau
            self.level_up()

    def level_up(self):
        """Augmente le niveau du joueur."""
        self.level += 1
        self.hp += 50  # Exemple de bonus de niveau
        self.mana += 20
        self.attack += 10
        self.defense += 5
        print(f"{self.name} a monté au niveau {self.level} !")


    @classmethod
    def from_dict(cls, data):
        """Charge les données du joueur à partir d'un dictionnaire."""
        return cls(
            name=data["name"],
            hp=data["hp"],
            mana=data["mana"],
            attack=data["attack"],
            defense=data["defense"],
            level=data["level"]
        )
    
    # data.py

class Boss:
    def __init__(self):
        self.name = "Boss Normal"
        self.hp = 500
        self.attack = 40
        self.defense = 20
        self.mana = 100

class FinalBoss(Boss):
    def __init__(self):
        super().__init__()
        self.name = "Boss Final"
        self.hp = 1000
        self.attack = 80
        self.defense = 50
        self.mana = 200

class Spell:
    def __init__(self, name, damage, mana_cost):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost


class Potion:
    def __init__(self, name, healing_amount):
        self.name = name
        self.healing_amount = healing_amount


class StatusEffect:
    def __init__(self, name, duration, effect):
        self.name = name
        self.duration = duration
        self.effect = effect


