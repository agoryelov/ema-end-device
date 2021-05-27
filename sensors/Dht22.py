
# installed Adafruit_DHT lib
import Adafruit_DHT

# GPIO lib
import RPi.GPIO as GPIO           # import RPi.GPIO module

# SensorInterface(Top Hierarchy)
# Author : clintonbf
# https://github.com/clintonbf/sensor_interface/blob/master/sensors/SensorInterface.py
from sensors.Dht import Dht

# unit conversion function
# Author : clintonbf
# https://github.com/clintonbf/sensor_interface/tree/master/unit_conversion
from utils.unit_conversion.temperature import celsius_to_kelvin

GPIO_IN = 4
MODEL_22 = 22

class Dht22(Dht):
    """
        Credit for connect_to_port and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """
    def __init__(self, uid: int, device: int = GPIO_IN) -> None:
        super().__init__(uid, device, model=MODEL_22)
    
    def get_data(self) -> dict:
        self.take_reading()
        readings = {
            "temperature ": self.get_temperature(),
            "relative_humidity": self.get_relative_humidity(),
        }
        return readings
