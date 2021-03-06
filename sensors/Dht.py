# inheritance library
# import abc
from utils.logger import log
import Adafruit_DHT
# GPIO lib
import RPi.GPIO as GPIO           # import RPi.GPIO module

from sensors.SensorException import SensorError, SensorReadError
from utils.unit_conversion.ConversionException import SensorUnitConversionError


# SensorInterface(Top Hierarchy)
# Author     : clintonbf
# Repository :   https://github.com/clintonbf/sensor_interface/blob/master/sensors/SensorInterface.py
from sensors.Sensor import Sensor

# unit conversion function
# Author     : clintonbf
# Repository : https://github.com/clintonbf/sensor_interface/tree/master/unit_conversion
from utils.unit_conversion.temperature import celsius_to_kelvin

DATA_INDICES = {
    "relative_humidity": 0,
    "temperature": 1,
}

class Dht(Sensor):
    """
        Credit for connect_to_port and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """
   
    def __init__(self, uid: int, device: str, model : int) -> None:
        self.__gpio_in = int(device)
        self.__model = model
        self.__reading = ()

    # Sets the GPIO to be in input mode
    def connect_to_sensor(self):
        DHT_in = self.__gpio_in
        GPIO.setmode(GPIO.BCM)
        try:
            GPIO.setup(DHT_in, GPIO.IN)  # set a port/pin as an input
        except:
            log('Error connecting to Dht sensor')
            return False
        
        return True

    # Take reading from the sensor
    # (with retry, it's guaranteed to get an output with up to 15 trials)
    def take_reading(self) -> int:
        try:
            self.__reading = Adafruit_DHT.read_retry(self.__model, self.__gpio_in)
            if(self.__reading[0] == None or self.__reading[1] == None):
                raise SensorError("Please check wiring")
        except:
            raise SensorReadError("Please check wiring")

    def get_raw_data(self)-> float:
        DHT_in = self.__gpio_in   
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        temp, humidity = Adafruit_DHT.read_retry(self.__model, DHT_in)

    def get_temperature(self) -> float:
        temperature_reading = 0.00
        try:
             temperature_reading = celsius_to_kelvin(self.__reading[DATA_INDICES['temperature']])
        except:
            raise SensorUnitConversionError("Cannot conver from Celsius to Kelvin, check input!")
        return temperature_reading

    # grab from self._reading, 
    # then take the field from the right index
    def get_relative_humidity(self) -> float:
        relative_humidity_reading =  0.00
        try :
            relative_humidity_reading = self.__reading[DATA_INDICES['relative_humidity']]
        except:
            raise SensorUnitConversionError("Cannot conver from Celsius to Kelvin, check input!")
        
        return relative_humidity_reading
    
