import paho.mqtt.client as mqtt


class RuuviSensorDataFormatException(Exception):
    pass


class RuuviSensorData:
    def __init__(self, bt_manufacturer_data):
        if bt_manufacturer_data is None or len(bt_manufacturer_data) == 0:
            raise RuuviSensorDataFormatException("No manufacturer data")

        if 0x0499 not in bt_manufacturer_data:
            raise RuuviSensorDataFormatException("No Ruuvi device")

        data = bt_manufacturer_data[0x0499]

        if data[0] == 0x03:
            # https://docs.ruuvi.com/communication/bluetooth-advertisements/data-format-3-rawv1
            if len(data) < 14:
                raise RuuviSensorDataFormatException("Data must be at least 14 bytes")

            self.humidity = data[1] * 0.5
            self.pressure = (data[4] * 256 + data[5]) + 50000
            self.battery_voltage = (data[12] * 256 + data[13]) / 1000
            if data[2] & 0b10000000:
                self.temperature = -(data[2] & 0b01111111) - data[3] / 100
            else:
                self.temperature = data[2] + data[3] / 100
        elif data[0] == 0x05:
            # https://docs.ruuvi.com/communication/bluetooth-advertisements/data-format-5-rawv2
            if len(data) != 24:
                raise RuuviSensorDataFormatException("Data must be 24 bytes")
            self.humidity = (data[3] * 256 + data[4]) * 0.0025
            self.pressure = (data[5] * 256 + data[6]) + 50000
            self.battery_voltage = ((data[13] * 256 + data[14]) >> 5) / 1000 + 1.6
            if data[1] & 0b10000000:
                self.temperature = (data[1] * 256 + data[2] - 65536) * 0.005
            else:
                self.temperature = (data[1] * 256 + data[2]) * 0.005
        else:
            raise RuuviSensorDataFormatException(f"Can't handle data format v{data[0]}")


class RuuviMqttConnection:
    def __init__(self, host, port=1883):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host, port)

    def send(self, name: str, data: RuuviSensorData):
        sanitized_name = name.replace(':', '_')

        self.mqtt_client.publish(topic=f"ruuvi/{sanitized_name}/temperature", payload=f"{data.temperature:.2f}")
        self.mqtt_client.publish(topic=f"ruuvi/{sanitized_name}/pressure", payload=f"{data.pressure:.2f}")
        self.mqtt_client.publish(topic=f"ruuvi/{sanitized_name}/humidity", payload=f"{data.humidity:.2f}")
        self.mqtt_client.loop_write(3)
