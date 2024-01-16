import unittest
from open_spiel.python.games.tiandijie.types import Attributes


class TestGenerateMaxLevelAttributes(unittest.TestCase):
    def test_generate_max_level_attributes(self):
        # Sample input attributes and growth coefficients
        initial_attributes = Attributes(166, 20, 23, 81, 34, 66)
        growth_coefficients = (24.96, 3.02, 3.49, 12.08, 5.1, 0.66)
        added_attributes = Attributes(0, 0, 0, 0, 0,
                                      0)  # Assuming all professions add the same attributes for simplicity

        # Call the function
        initial_attributes.generate_max_level_attributes(growth_coefficients, 'SORCERER_DAMAGE')
        initial_attributes.multiply_attributes('SORCERER_DAMAGE')

        # Assert that the results are as expected
        self.assertEqual(initial_attributes.life, 5808)
        self.assertEqual(initial_attributes.attack, 404)
        self.assertEqual(initial_attributes.defense, 1042)
        self.assertEqual(initial_attributes.magic_attack, 3013)
        self.assertEqual(initial_attributes.magic_defense, 1433)
        self.assertEqual(initial_attributes.luck, 222)


if __name__ == '__main__':
    unittest.main()
