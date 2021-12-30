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

    def find_ruuvi_data(self, manufacturer_data: dict):
        if manufacturer_data is None or len(manufacturer_data) == 0:
            return None

        if 0x0499 in manufacturer_data:
            data = manufacturer_data[0x0499]
            try:
                return RuuviSensorData(data)
            except RuuviSensorDataFormatException:
                return None

        return None

    def detection_callback(self, device, advertisement_data):
        ruuvi_data = self.find_ruuvi_data(advertisement_data.manufacturer_data)
        if ruuvi_data is not None:
            self.mqtt_connection.send(device.address, ruuvi_data)

    async def run(self):
        scanner = BleakScanner()
        scanner.register_detection_callback(self.detection_callback)
        await scanner.start()

        while not self.quit_event.is_set():
            sleep(1)

        await scanner.stop()


runner = Runner()
signal.signal(signal.SIGINT, runner.sigterm_handler)
asyncio.run(runner.run())
