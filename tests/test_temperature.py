from unittest import TestCase
from sensor_interface.unit_conversion.temperature import celsius_to_kelvin
from sensor_interface.unit_conversion.temperature import fahrenheit_to_kelvin


class Test(TestCase):
    def test_celsius_to_kelvin(self):
        celsius_temp = 100
        kelvin_temp = 373.15

        self.assertEqual(celsius_to_kelvin(celsius_temp), kelvin_temp)

    def test_celsius_absolute_zero(self):
        temp = -500

        with self.assertRaises(ValueError):
            celsius_to_kelvin(temp)

    def test_fahrenheit_to_kelvin(self):
        fahrenheit_temp = 212
        kelvin_temp = 373.15

        self.assertEqual(fahrenheit_to_kelvin(fahrenheit_temp), kelvin_temp)

    def test_fahrenheit_absolute_zero(self):
        temp = -500

        with self.assertRaises(ValueError):
            fahrenheit_to_kelvin(temp)