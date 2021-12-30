import paho.mqtt.client as mqtt


class RuuviSensorDataFormatException(Exception):
    pass


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


