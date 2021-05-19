# inheritance library
# import abc
import Adafruit_DHT
# GPIO lib
import RPi.GPIO as GPIO           # import RPi.GPIO module


# SensorInterface(Top Hierarchy)
# Author     : clintonbf
# Repository :   https://github.com/clintonbf/sensor_interface/blob/master/sensors/SensorInterface.py
from sensors import Sensor

# unit conversion function
# Author     : clintonbf
# Repository : https://github.com/clintonbf/sensor_interface/tree/master/unit_conversion
from unit_conversion import celsius_to_kelvin

DATA_INDICES = {
    "relative_humidity": 0,
        "temperature": 1,
    }

class Dht(Sensor):
    """
        Credit for connect_to_port and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """

    # TODO: what is timeout ?
    # TODO: It is just a GPIO data in, not serial connection.
    # TODO: pass it in like : gpio_in = 1, named params
   
    def __init__(self, uid: int, gpio_in: str, model : str ) -> None:
        # super().__init__()
        self.__uid = uid
        self.__gpio_in = gpio_in
        # self.__timeout = timeout
        if model.lower() == 'dht11':
            self.__model = 11
        # elif model.lower() == 'am2302':
        #     self.__model = 22
        else:
            self.__model = 22
        self.__reading = () # TODO meaning?

    @classmethod
    def __subclasshook__(cls, subclass):
        return(hasattr(subclass, 'format_data') and
               callable(subclass.format_data) or
               NotImplemented)

    # Sets the GPIO to be in input mode
    def connect_to_sensor(self) -> int:
        DHT_in = self.__gpio_in
        # TODO return a value for error checking?
        GPIO.setmode(GPIO.BCM)                 # choose BCM or BOARD
        status = GPIO.setup(DHT_in, GPIO.IN)  # set a port/pin as an input
        return status

    # Take reading from the sensor
    # (with retry, it's garunteed to get an output with up to 15 trials )
    def take_reading(self) -> int:     
        self.__reading = Adafruit_DHT.read_retry(self.__model, self.__gpio_in)


    # TODO: necessary?
    def get_raw_data(self)-> float:
        DHT_in = self.__gpio_in   
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        temp, humidity = Adafruit_DHT.read_retry(self.__model, DHT_in)

    def get_temperature(self) -> float:
        # return celsius_to_kelvin(float(Adafruit_DHT.read_retry(self.__model,self.__gpio_in)[1]))
        return celsius_to_kelvin(self.__reading[DATA_INDICES['temperature']])

    # grab from self._reading, 
    # then take the field from the right index
    def get_relative_humidity(self) -> float:
        return self.__reading[DATA_INDICES['relative_humidity']]
    
   
