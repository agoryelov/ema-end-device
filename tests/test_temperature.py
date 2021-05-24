from unittest import TestCase
from utils.unit_conversion.temperature import *


class Test(TestCase):
    def test_celsius_to_kelvin(self):
        celsius_temp = 100
        kelvin_temp = 373.15

        self.assertEqual(celsius_to_kelvin(celsius_temp), kelvin_temp)

    def test_fahrenheit_to_kelvin(self):
        fahrenheit_temp = 212
        kelvin_temp = 373.15

        self.assertEqual(fahrenheit_to_kelvin(fahrenheit_temp), kelvin_temp)
