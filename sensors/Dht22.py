
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

from sensors.SensorDataFormatter import SensorDataFormatter

class Dht22(Dht, SensorDataFormatter):
    """
        Credit for connect_to_port and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """
    def __init__(self, uid: int, gpio_in: int,  model : str ) -> None:
        super().__init__(uid,gpio_in,model)
        self.__uid = uid
        self.__gpio_in = gpio_in
        
        # DHT22:
        self.__model = 22
        self.__reading = ()
        
    # Sets the GPIO to be in input mode
    def connect_to_sensor(self):
        DHT_in = self.__gpio_in
        # TODO error checking?
        GPIO.setmode(GPIO.BCM)                 # choose BCM or BOARD
        status = GPIO.setup(DHT_in, GPIO.IN)  # set a port/pin as an input
        return status
    
    def get_uid(self):
        return self.__uid
    
    def format_data(self) -> dict :
        readings = {
            "uid": self.get_uid(),
            "temperature ": self.get_temperature(),
            "relative_humidity": self.get_relative_humidity(),
        }
        return readings
