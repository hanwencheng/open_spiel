from typing import Tuple

from open_spiel.python.games.tiandijie.basicAttributes import JishenProfessions, ShenbinProfessions, HuazhenProfessions, \
    XingpanProfessions, HuazhenAmplifier, XingpanAmplifier
from open_spiel.python.games.tiandijie.wunei import WuneiProfessions

MAXIMUM_LEVEL = 70
WUNEI_AMPLIFIERS = (25, 25, 25, 25, 25, 0)
JISHEN_AMPLIFIERS = (10, 0, 10, 0, 10, 0)
XINGYAO_AMPLIFIERS = (4, 4, 4, 4, 4, 0)


def calculateMaxAddedValue(wuneiProfession, jishenProfession, shenbinProfession,
                           huazhenProfession, xingpan_profession):
    print('profession is', [jishenProfession, shenbinProfession, huazhenProfession, wuneiProfession])

    calculated_values = tuple(
        jishenProfession[i] +
        shenbinProfession[i] * (69 / 10 + 1) +
        huazhenProfession[i] +
        sum(wuneiProfession[i]) +
        xingpan_profession[i]
        for i in range(6)
    )

    return calculated_values


def get_enum_value(enum_class, identifier):
    if isinstance(identifier, int):
        # Fetch by index
        return list(enum_class)[identifier].value[1:]
    elif isinstance(identifier, str):
        # Fetch by name
        return enum_class[identifier].value[1:]
    else:
        raise ValueError("Identifier must be an enum name or index")


class ProfessionAttributes:
    def __init__(self, wunei, jishen, shenbin, huazhen, xingpan, huazhen_amp, xingpan_amp):
        self.wunei = wunei
        self.jishen = jishen
        self.shenbin = shenbin
        self.huazhen = huazhen
        self.xingpan = xingpan
        self.huazhen_amp = huazhen_amp
        self.xingpan_amp = xingpan_amp


def get_profession_values(profession_identifier):
    wunei = get_enum_value(WuneiProfessions, profession_identifier)
    jishen = get_enum_value(JishenProfessions, profession_identifier)
    shenbin = get_enum_value(ShenbinProfessions, profession_identifier)
    huazhen = get_enum_value(HuazhenProfessions, profession_identifier)
    xingpan = get_enum_value(XingpanProfessions, profession_identifier)
    huazhen_amp = get_enum_value(HuazhenAmplifier, profession_identifier)
    xingpan_amp = get_enum_value(XingpanAmplifier, profession_identifier)

    # Assuming you want to return these as a single object (like a dictionary)
    return ProfessionAttributes(wunei, jishen, shenbin, huazhen, xingpan, huazhen_amp, xingpan_amp)


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
            identifier
    ):
        profession_values = get_profession_values(identifier)
        added_attributes_tuple = calculateMaxAddedValue(profession_values.wunei, profession_values.jishen,
                                                        profession_values.shenbin,
                                                        profession_values.huazhen, profession_values.xingpan)
        attribute_names = ['life', 'attack', 'defense', 'magic_attack', 'magic_defense', 'luck']
        for attr_name, growth_coefficient, added_value in zip(attribute_names, growth_coefficient_tuple,
                                                              added_attributes_tuple):
            current_value = getattr(self, attr_name)
            setattr(self, attr_name, current_value + MAXIMUM_LEVEL * growth_coefficient + added_value)

    def multiply_attributes(self, identifier):
        attribute_names = ['life', 'attack', 'defense', 'magic_attack', 'magic_defense', 'luck']
        profession_values = get_profession_values(identifier)
        xingpan_amplifiers = profession_values.xingpan_amp
        huazhen_amplifiers = profession_values.huazhen_amp
        for attr_name, xingpan_amplifier, huazhen_amplifier, wunei_amplifier, jishen_amplifier, xingyao_amplifier in zip(
                attribute_names, xingpan_amplifiers,
                huazhen_amplifiers, WUNEI_AMPLIFIERS, JISHEN_AMPLIFIERS, XINGYAO_AMPLIFIERS):
            current_value = getattr(self, attr_name)
            setattr(self, attr_name, round(current_value * (
                    1 + xingpan_amplifier / 100 + huazhen_amplifier / 100 + wunei_amplifier / 100 + jishen_amplifier / 100 + xingyao_amplifier / 100)))
