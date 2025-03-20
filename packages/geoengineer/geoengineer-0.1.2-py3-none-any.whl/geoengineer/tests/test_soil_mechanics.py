import unittest
from geoengineer import effective_stress

class TestSoilMechanics(unittest.TestCase):
    def test_effective_stress(self):
        # Test case 1: Basic calculation
        self.assertEqual(effective_stress(100, 40), 60)
        
        # Test case 2: Zero pore water pressure
        self.assertEqual(effective_stress(100, 0), 100)
        
        # Test case 3: Negative effective stress (uplift condition)
        self.assertEqual(effective_stress(50, 70), -20)
        
        # Test case 4: Floating point values
        self.assertAlmostEqual(effective_stress(125.5, 45.3), 80.2)

if __name__ == "__main__":
    unittest.main() 