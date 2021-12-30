import unittest

from ruuvi.RuuviSensorData import RuuviSensorData


class RuuviSensorDataTest(unittest.TestCase):
    def test_construction_v3_valid_data(self):
        sut = RuuviSensorData([0x03, 0x29, 0x1A, 0x1E, 0xCE, 0x1E, 0xFC, 0x18, 0xF9, 0x42, 0x02, 0xCA, 0x0B, 0x53])
        self.assertAlmostEqual(sut.pressure, 102766, 6)
        self.assertAlmostEqual(sut.humidity, 20.5, 6)
        self.assertAlmostEqual(sut.temperature, 26.3, 6)
        self.assertAlmostEqual(sut.battery_voltage, 2.899, 6)

    def test_construction_v3_maximum_values(self):
        sut = RuuviSensorData([0x03, 0xFF, 0x7F, 0x63, 0xFF, 0xFF, 0x7F, 0xFF, 0x7F, 0xFF, 0x7F, 0xFF, 0xFF, 0xFF])
        self.assertAlmostEqual(sut.pressure, 115535, 6)
        self.assertAlmostEqual(sut.humidity, 127.5, 6)
        self.assertAlmostEqual(sut.temperature, 127.99, 6)
        self.assertAlmostEqual(sut.battery_voltage, 65.535, 6)

    def test_construction_v3_minumum_values(self):
        sut = RuuviSensorData([0x03, 0x00, 0xFF, 0x63, 0x00, 0x00, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x00, 0x00])
        self.assertAlmostEqual(sut.pressure, 50000, 6)
        self.assertAlmostEqual(sut.humidity, 0.0, 6)
        self.assertAlmostEqual(sut.temperature, -127.99, 6)
        self.assertAlmostEqual(sut.battery_voltage, 0.0, 6)


if __name__ == '__main__':
    unittest.main()
