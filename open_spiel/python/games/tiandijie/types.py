class Attributes(tuple):
    def __new__(cls, life, attack, defense, magic_attack, magic_defense, luck):
        return super(Attributes, cls).__new__(cls, (life, attack, defense, magic_attack, magic_defense, luck))

    def __init__(self, life, attack, defense, magic_attack, magic_defense, luck):
        self.values = (life, attack, defense, magic_attack, magic_defense, luck)  # This is the tuple
        self.life = life
        self.attack = attack
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense
        self.luck = luck

    def __len__(self):
        return 6

    def __getitem__(self, index):
        return self.values[index]  # Implement subscriptability directly on the class

    @property
    def value(self):
        return self.values

    def multiply_attributes(self, factor):
        for attr in ['life', 'attack', 'defense', 'magic_attack', 'magic_defense', 'luck']:
            current_value = getattr(self, attr)
            if isinstance(current_value, (float, int)):
                setattr(self, attr, current_value * factor)


def multiply_attributes(self, factor):
    for attr in ['life', 'attack', 'defense', 'magic_attack', 'magic_defense', 'luck']:
        current_value = getattr(self, attr)
        if isinstance(current_value, (float, int)):
            setattr(self, attr, current_value * factor)
