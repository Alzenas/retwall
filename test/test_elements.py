import unittest
import structural.elements as e


class TestElements(unittest.TestCase):
    def test_soil_ka_phi0(self):
        test_soil = e.Soil()
        test_soil.phi = 0
        result = test_soil.ka()[0]
        self.assertEqual(result, 1)

    def test_soil_ka_phi90(self):
        test_soil = e.Soil("Test Soil")
        test_soil.phi = 90
        result = test_soil.ka()[0]
        self.assertEqual(result, 0)

    def test_soil_kp_phi0(self):
        test_soil = e.Soil()
        test_soil.phi = 0
        result = test_soil.kp()[0]
        self.assertEqual(result, 1)

    def test_soil_kp_phi30(self):
        test_soil = e.Soil("Test Soil")
        test_soil.phi = 30
        result = test_soil.kp()[0]
        self.assertEqual(result, 3)

    def test_soil_kp_phi90(self):
        test_soil = e.Soil()
        test_soil.phi = 90
        result = test_soil.kp()[0]
        self.assertEqual(result, 999)

    def test_soil_kp_phi180(self):
        test_soil = e.Soil()
        test_soil.phi = 180
        result = test_soil.kp()[0]
        self.assertEqual(result, 999)

    def test_soil_k0_phi30(self):
        test_soil = e.Soil()
        test_soil.phi = 30
        result = test_soil.k0()[0]
        self.assertEqual(result, 0.5)

    def test_soil_k0_phi0(self):
        test_soil = e.Soil()
        test_soil.phi = 0
        result = test_soil.k0()[0]
        self.assertEqual(result, 1)

    def test_soil_k0_phi90(self):
        test_soil = e.Soil()
        test_soil.phi = 90
        result = test_soil.k0()[0]
        self.assertEqual(result, 0)


if __name__ == '__main--':
    # run the tests
    unittest.main()
