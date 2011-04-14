import unittest
from cel_to_far import convert


class ValidTempConversion(unittest.TestCase):

    known_values = (
        (-50, -58),
        (0, 32),
        (13, 55.4),
        (50, 122),
        (100, 212),
    )

    def testConversion(self):
        """Tests the conversion from celsius to fahrenheit"""
        for celsius, fahrenheit in self.known_values:
            result = convert(celsius)
            self.assertAlmostEqual(fahrenheit, result)


class BadInputConversion(unittest.TestCase):

    def testNonNumericInput(self):
        """Conversion should fail for non numeric input"""
        self.assertRaises(TypeError, convert, 'ABCD')


if __name__ == '__main__':
    unittest.main()
