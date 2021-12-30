from RuuviSensorDataFormatException import RuuviSensorDataFormatException


class RuuviSensorData:
    def __init__(self, bt_manufacturer_data):
        if bt_manufacturer_data[0] == 0x03:
            if len(bt_manufacturer_data) < 14:
                raise RuuviSensorDataFormatException("Data must be at least 14 bytes")

            self.humidity = bt_manufacturer_data[1] * 0.5
            self.pressure = (bt_manufacturer_data[4] * 256 + bt_manufacturer_data[5]) + 50000
            self.battery_voltage = (bt_manufacturer_data[12] * 256 + bt_manufacturer_data[13]) / 1000
            if bt_manufacturer_data[2] & 0b10000000:
                self.temperature = -(bt_manufacturer_data[2] & 0b01111111) - bt_manufacturer_data[3] / 100
            else:
                self.temperature = bt_manufacturer_data[2] - bt_manufacturer_data[3] / 100
        else:
            raise RuuviSensorDataFormatException(f"Can't handle data format v{bt_manufacturer_data[0]}")
