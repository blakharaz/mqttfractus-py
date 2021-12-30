#!/usr/bin/env python3

import asyncio
import signal
import threading

from bleak import BleakScanner
from time import sleep

from ruuvi import *


class Runner:
    def __init__(self):
        self.quit_event = threading.Event()
        self.mqtt_connection = RuuviMqttConnection("odroid")

    def sigterm_handler(self, _signo, _stack_frame):
        self.quit_event.set()

    @staticmethod
    def find_ruuvi_data(manufacturer_data: dict):
        try:
            return RuuviSensorData(manufacturer_data)
        except RuuviSensorDataFormatException:
            return None

    def detection_callback(self, device, advertisement_data):
        ruuvi_data = self.find_ruuvi_data(advertisement_data.manufacturer_data)
        if ruuvi_data is not None:
            self.mqtt_connection.send(device.address, ruuvi_data)

    async def run(self):
        scanner = BleakScanner()
        scanner.register_detection_callback(self.detection_callback)

        while not self.quit_event.is_set():
            await scanner.start()
            sleep(15)
            await scanner.stop()


runner = Runner()
signal.signal(signal.SIGINT, runner.sigterm_handler)
asyncio.run(runner.run())
