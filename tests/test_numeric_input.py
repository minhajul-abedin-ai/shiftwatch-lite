import unittest
from shiftwatch.core import _clean


class NumericInputTests(unittest.TestCase):
    def test_oversized_integer_has_documented_error(self):
        with self.assertRaisesRegex(ValueError, 'finite numeric'):
            _clean([10 ** 400])

    def test_normal_numeric_values_remain_accepted(self):
        self.assertEqual(_clean([1, 2.5]), [1.0, 2.5])

    def test_nonfinite_float_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'finite numeric'):
            _clean([float('inf')])


if __name__ == '__main__':
    unittest.main()
