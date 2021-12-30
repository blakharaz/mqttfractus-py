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
            if len(data) < 14:
                raise RuuviSensorDataFormatException("Data must be at least 14 bytes")

            self.humidity = data[1] * 0.5
            self.pressure = (data[4] * 256 + data[5]) + 50000
            self.battery_voltage = (data[12] * 256 + data[13]) / 1000
            if data[2] & 0b10000000:
                self.temperature = -(data[2] & 0b01111111) - data[3] / 100
            else:
                self.temperature = data[2] - data[3] / 100
        else:
            raise RuuviSensorDataFormatException(f"Can't handle data format v{bt_manufacturer_data[0]}")


class RuuviMqttConnection:
    def __init__(self, host, port=1883):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host, port)

    def send(self, name: str, data: RuuviSensorData):
        sanitized_name = name.replace(':', '_')

        self.mqtt_client.publish(topic=f"ruuvi/{sanitized_name}/temperature", payload=data.temperature)
        self.mqtt_client.publish(topic=f"ruuvi/{sanitized_name}/pressure", payload=data.pressure)
        self.mqtt_client.publish(topic=f"ruuvi/{sanitized_name}/humidity", payload=data.humidity)
        self.mqtt_client.loop_write(10)
