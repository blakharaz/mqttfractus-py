#!/usr/bin/env python3

import asyncio
import signal
import threading

from bleak import BleakScanner
from time import sleep

from RuuviMqttConnection import RuuviMqttConnection
from RuuviSensorData import RuuviSensorData
from RuuviSensorDataFormatException import RuuviSensorDataFormatException


def sigterm_handler(_signo, _stack_frame):
    quit_event.set()


def find_ruuvi_data(manufacturer_data: dict):
    if manufacturer_data is None or len(manufacturer_data) == 0:
        return None

    if 0x0499 in manufacturer_data:
        data = manufacturer_data[0x0499]
        try:
            return RuuviSensorData(data)
        except RuuviSensorDataFormatException:
            return None

    return None


def detection_callback(device, advertisement_data):
    ruuvi_data = find_ruuvi_data(advertisement_data.manufacturer_data)
    if ruuvi_data is not None:
        print(f"{device.address}: {ruuvi_data.temperature}C {ruuvi_data.humidity}% {ruuvi_data.pressure}mPa")


async def main():
    global mqtt_connection
    mqtt_connection = RuuviMqttConnection("odroid")
    mqtt_connection.send(
        "wohnzimmer",
        RuuviSensorData([0x03, 0x29, 0x1A, 0x1E, 0xCE, 0x1E, 0xFC, 0x18, 0xF9, 0x42, 0x02, 0xCA, 0x0B, 0x53]))
#     signal.signal(signal.SIGINT, sigterm_handler)
#
#     scanner = BleakScanner()
#     scanner.register_detection_callback(detection_callback)
#     await scanner.start()
#
#     while not quit_event.is_set():
#         sleep(1)
#
#     await scanner.stop()

quit_event = threading.Event()
mqtt_connection = None
asyncio.run(main())
