from unittest import TestCase
import serial
from serial import SerialException


class TestSpecDgs(TestCase):
    def test_missing_device_raises_exception(self):
        DEVICE = '/dev/ttyUSB0'
        TIMEOUT = 3
        BAUD_RATE = 9600

        with self.assertRaises(SerialException):
            ser = serial.Serial(DEVICE, BAUD_RATE, timeout=TIMEOUT, parity=serial.PARITY_NONE)

    def test_connect_to_sensor(self):
        DEVICE = '/dev/ttyUSB0'
        TIMEOUT = 3
        BAUD_RATE = 9600

        ser = serial.Serial(DEVICE, BAUD_RATE, timeout=TIMEOUT, parity=serial.PARITY_NONE)

        self.assertIsInstance(ser, serial.Serial)
