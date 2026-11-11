import math
import unittest
from shiftwatch import drift_report, psi, js_divergence

class DriftTests(unittest.TestCase):
    def test_identical(self):
        r = drift_report(range(100), range(100))
        self.assertAlmostEqual(r['psi'], 0)
        self.assertAlmostEqual(r['js_divergence_nats'], 0)

    def test_shift(self):
        r = drift_report(range(100), range(100,200))
        self.assertGreater(r['psi'], 0)
        self.assertGreater(r['js_divergence_nats'], 0)
        self.assertLessEqual(r['js_divergence_nats'], math.log(2))

    def test_constant_reference(self):
        r = drift_report([5]*20, [6]*20)
        self.assertEqual(r['effective_bins'], 2)

    def test_invalid_values(self):
        for bad in ([float('nan')], [True], []):
            with self.assertRaises(ValueError):
                drift_report(bad, [1])

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            psi([0,0],[1,0])
        with self.assertRaises(ValueError):
            js_divergence([1],[1,2])

    def test_bins(self):
        with self.assertRaises(ValueError):
            drift_report([1,2],[1,2], n_bins=1)

if __name__ == '__main__':
    unittest.main()
