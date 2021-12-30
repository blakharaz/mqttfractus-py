import paho.mqtt.client as mqtt

from RuuviSensorData import RuuviSensorData


class RuuviMqttConnection:
    def __init__(self, host, port=1883):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host, port)

    def send(self, name: str, data: RuuviSensorData):
        self.mqtt_client.publish(topic=f"ruuvi/{name}/temperature", payload=data.temperature)
        self.mqtt_client.publish(topic=f"ruuvi/{name}/pressure", payload=data.pressure)
        self.mqtt_client.publish(topic=f"ruuvi/{name}/humidity", payload=data.humidity)
        self.mqtt_client.loop_write(10)
