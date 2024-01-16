import unittest

from open_spiel.python.games.tiandijie.basicAttributes import JishenProfessions, ShenbinProfessions, HuazhenProfessions, \
    XingpanProfessions, HuazhenAmplifier, XingpanAmplifier
from open_spiel.python.games.tiandijie.types import Attributes
from open_spiel.python.games.tiandijie.wunei import WuneiProfessions


class TestGenerateMaxLevelAttributes(unittest.TestCase):
    def test_generate_max_level_attributes(self):
        # Sample input attributes and growth coefficients
        initial_attributes = Attributes(166, 20, 23, 81, 34, 66)
        growth_coefficients = (24.96, 3.02, 3.49, 12.08, 5.1, 0.66)
        added_attributes = Attributes(0, 0, 0, 0, 0,
                                      0)  # Assuming all professions add the same attributes for simplicity

        wuneiProfession = WuneiProfessions.SORCERER_DAMAGE
        jishenProfession = JishenProfessions.SORCERER_DAMAGE
        shenbinProfession = ShenbinProfessions.SORCERER_DAMAGE
        huazhenProfessions = HuazhenProfessions.SORCERER_DAMAGE
        xingppanProfessions = XingpanProfessions.SORCERER_DAMAGE
        huazhenAmplifier = HuazhenAmplifier.SORCERER_DAMAGE
        xingpanAmplifier = XingpanAmplifier.SORCERER_DAMAGE

        # Call the function
        initial_attributes.generate_max_level_attributes(growth_coefficients, wuneiProfession,
                                                       jishenProfession, shenbinProfession, huazhenProfessions, xingppanProfessions)

        initial_attributes.multiply_attributes(huazhenAmplifier, xingpanAmplifier)

        # Expected results
        expected_life = 5808
        expected_attack = 404
        expected_defense = 1042
        expected_magic_attack = 3013
        expected_magic_defense = 1433
        expected_luck = 222
        print(initial_attributes)

        # Assert that the results are as expected
        self.assertEqual(initial_attributes.life, expected_life)
        self.assertEqual(initial_attributes.attack, expected_attack)
        self.assertEqual(initial_attributes.defense, expected_defense)
        self.assertEqual(initial_attributes.magic_attack, expected_magic_attack)
        self.assertEqual(initial_attributes.magic_defense, expected_magic_defense)
        self.assertEqual(initial_attributes.luck, expected_luck)


if __name__ == '__main__':
    unittest.main()
