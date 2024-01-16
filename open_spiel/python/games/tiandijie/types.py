from typing import Tuple

MAXIMUM_LEVEL = 70
WUNEI_AMPLIFIERS = (25, 25, 25, 25, 25, 0)
JISHEN_AMPLIFIERS = (10, 0, 10, 0, 10, 0)
XINGYAO_AMPLIFIERS = (4, 4, 4, 4, 4, 0)


def calculateMaxAddedValue(wuneiProfession, jishenProfession, shenbinProfession,
                           huazhenProfession, xingpan_profession):
    print('profession is', [jishenProfession, shenbinProfession, huazhenProfession, wuneiProfession])

    calculated_values = tuple(
        jishenProfession.value[i] +
        shenbinProfession.value[i] * (69 / 10 + 1) +
        huazhenProfession.value[i] +
        sum(wuneiProfession.value[i]) +
        xingpan_profession.value[i]
        for i in range(6)
    )

    return calculated_values


class Attributes(tuple):
    def __new__(cls, life, attack, defense, magic_attack, magic_defense, luck):
        return super(Attributes, cls).__new__(cls, (life, attack, defense, magic_attack, magic_defense, luck))

    def __init__(self, life, attack, defense, magic_attack, magic_defense, luck):
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

    def generate_max_level_attributes(
            self,
            growth_coefficient_tuple: Tuple,
            wunei_profession: Tuple[float, float, float, float, float, float],
            jishen_profession: Tuple[float, float, float, float, float, float],
            shenbin_profession: Tuple[float, float, float, float, float, float],
            huazhen_profession: Tuple[float, float, float, float, float, float],
            xingpan_profession: Tuple[float, float, float, float, float, float]
    ):
        added_attributes_tuple = calculateMaxAddedValue(wunei_profession, jishen_profession, shenbin_profession,
                                                        huazhen_profession, xingpan_profession)
        attribute_names = ['life', 'attack', 'defense', 'magic_attack', 'magic_defense', 'luck']
        print('growth coefficient', growth_coefficient_tuple)
        print('added attributes', added_attributes_tuple)
        for attr_name, growth_coefficient, added_value in zip(attribute_names, growth_coefficient_tuple,
                                                              added_attributes_tuple):
            current_value = getattr(self, attr_name)
            setattr(self, attr_name, current_value + MAXIMUM_LEVEL * growth_coefficient + added_value)

    def multiply_attributes(self, huazhen_amplifiers, xingpan_amplifiers):
        attribute_names = ['life', 'attack', 'defense', 'magic_attack', 'magic_defense', 'luck']
        for attr_name, xingpan_amplifier, huazhen_amplifier, wunei_amplifier, jishen_amplifier, xingyao_amplifier in zip(
                attribute_names, xingpan_amplifiers.value[1:],
                huazhen_amplifiers.value[1:], WUNEI_AMPLIFIERS, JISHEN_AMPLIFIERS, XINGYAO_AMPLIFIERS):
            current_value = getattr(self, attr_name)
            setattr(self, attr_name, round(current_value * (
                        1 + xingpan_amplifier/100 + huazhen_amplifier/100 + wunei_amplifier/100 + jishen_amplifier/100 + xingyao_amplifier/100)))
