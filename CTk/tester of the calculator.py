import unittest
from really_stupid_calculator_that_gets_only_squares_of_repeating_nines import square_of_repeating_nines

class TestSquareOfRepeatingNines(unittest.TestCase):
    def test_valid_repeating_nines(self):
        test_cases = {
            "9": 81,
            "99": 9801,
            "999": 998001,
            "9999": 99980001,
            "99999": 9999800001,
            "999999": 999998000001,
            "9999999": 99999980000001,
            "99999999": 9999999800000001,
            "999999999": 999999998000000001,
            "9999999999": 99999999980000000001,
        }

        for inp, expected in test_cases.items():
            with self.subTest(inp=inp):
                self.assertEqual(square_of_repeating_nines(inp), expected)

    def test_many_nines(self):
        for i in range(1, 91):  # up to 90 digits
            inp = "9" * i
            expected = int(inp)**2
            with self.subTest(inp=inp):
                self.assertEqual(square_of_repeating_nines(inp), expected)

    def test_invalid_inputs(self):
        invalids = [
            "1", "91", "98", "123", "abc", "", "0009", "99a", "9 9",
            998, 909, 9991, "9a9", "8899", "911", "9998", "9009"
        ]
        for val in invalids:
            with self.subTest(val=val):
                self.assertFalse(square_of_repeating_nines(val))

if __name__ == "__main__":
    unittest.main()