import unittest

from ruuvi import RuuviSensorData


class RuuviSensorDataTest(unittest.TestCase):
    def test_construction_v3_valid_data(self):
        sut = RuuviSensorData(
            {0x0499: [0x03, 0x29, 0x1A, 0x1E, 0xCE, 0x1E, 0xFC, 0x18, 0xF9, 0x42, 0x02, 0xCA, 0x0B, 0x53]})
        self.assertAlmostEqual(sut.pressure, 102766, 6)
        self.assertAlmostEqual(sut.humidity, 20.5, 6)
        self.assertAlmostEqual(sut.temperature, 26.3, 6)
        self.assertAlmostEqual(sut.battery_voltage, 2.899, 6)

    def test_construction_v3_maximum_values(self):
        sut = RuuviSensorData(
            {0x0499: [0x03, 0xFF, 0x7F, 0x63, 0xFF, 0xFF, 0x7F, 0xFF, 0x7F, 0xFF, 0x7F, 0xFF, 0xFF, 0xFF]})
        self.assertAlmostEqual(sut.pressure, 115535, 6)
        self.assertAlmostEqual(sut.humidity, 127.5, 6)
        self.assertAlmostEqual(sut.temperature, 127.99, 6)
        self.assertAlmostEqual(sut.battery_voltage, 65.535, 6)

    def test_construction_v3_minumum_values(self):
        sut = RuuviSensorData(
            {0x0499: [0x03, 0x00, 0xFF, 0x63, 0x00, 0x00, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x00, 0x00]})
        self.assertAlmostEqual(sut.pressure, 50000, 6)
        self.assertAlmostEqual(sut.humidity, 0.0, 6)
        self.assertAlmostEqual(sut.temperature, -127.99, 6)
        self.assertAlmostEqual(sut.battery_voltage, 0.0, 6)

    def test_construction_v5_valid_data(self):
        sut = RuuviSensorData(
            {0x0499: [0x05, 0x12, 0xFC, 0x53, 0x94, 0xC3, 0x7C, 0x00, 0x04, 0xFF, 0xFC, 0x04, 0x0C, 0xAC, 0x36, 0x42,
                      0x00, 0xCD, 0xCB, 0xB8, 0x33, 0x4C, 0x88, 0x4F]})
        self.assertAlmostEqual(sut.pressure, 100044, 6)
        self.assertAlmostEqual(sut.humidity, 53.49, 6)
        self.assertAlmostEqual(sut.temperature, 24.3, 6)
        self.assertAlmostEqual(sut.battery_voltage, 2.977, 6)

    def test_construction_v5_maximum_values(self):
        sut = RuuviSensorData(
            {0x0499: [0x05, 0x7F, 0xFF, 0xFF, 0xFE, 0xFF, 0xFE, 0x7F, 0xFF, 0x7F, 0xFF, 0x7F, 0xFF, 0xFF, 0xDE, 0xFE,
                      0xFF, 0xFE, 0xCB, 0xB8, 0x33, 0x4C, 0x88, 0x4F]})
        self.assertAlmostEqual(sut.pressure, 115534, 6)
        self.assertAlmostEqual(sut.humidity, 163.835, 6)
        self.assertAlmostEqual(sut.temperature, 163.835, 6)
        self.assertAlmostEqual(sut.battery_voltage, 3.646, 6)

    def test_construction_v5_minumum_values(self):
        sut = RuuviSensorData(
            {0x0499: [0x05, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x00, 0x00, 0x00,
                      0x00, 0x00, 0xCB, 0xB8, 0x33, 0x4C, 0x88, 0x4F]})
        self.assertAlmostEqual(sut.pressure, 50000, 6)
        self.assertAlmostEqual(sut.humidity, 0.0, 6)
        self.assertAlmostEqual(sut.temperature, -163.835, 6)
        self.assertAlmostEqual(sut.battery_voltage, 1.600, 6)


if __name__ == '__main__':
    unittest.main()
