# inheritance library
import abc

# installed Adafruit_DHT lib
import Adafruit_DHT

# GPIO lib
import RPi.GPIO as GPIO           # import RPi.GPIO module


# SensorInterface(Top Hierarchy)
# Author : clintonbf
# https://github.com/clintonbf/sensor_interface/blob/master/sensors/SensorInterface.py
from sensors import SensorInterface

# unit conversion function
# Author : clintonbf
# https://github.com/clintonbf/sensor_interface/tree/master/unit_conversion
from unit_conversion import celsius_to_kelvin


DATA_INDICES = {
    "serial_number": 0,
    "measurement": 1,
    "temperature": 2,
    "relative_humidity": 3,
    "raw_sensor": 4,
    "temp_digital": 5,
    "rh_digital": 6,
    "day": 7,
    "hour": 8,
    "minute": 9,
    "second": 10
}


class DHT(SensorInterface, metaclass=abc.ABCMeta):
    """
        Credit for connect_to_port and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """

    def __init__(self, uid: int, gpio_in: int,  model : str ) -> None:
        super().__init__()
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


    # Sets the GPIO to be in input mode
    def connect_to_port(self) -> int:
        DHT_in = self.__gpio_in
        # TODO error checking?
        GPIO.setmode(GPIO.BCM)                 # choose BCM or BOARD
        status = GPIO.setup(DHT_in, GPIO.IN)  # set a port/pin as an input
        return status

    # take reading:
    def take_reading(self) -> int:
        DHT_in = self.__device
        # TODO error checking?
        GPIO.setmode(GPIO.BCM)                 # choose BCM or BOARD
        Adafruit_DHT.read(self.__, DHT_PIN)

    # TODO : no raw data or the raw data is dealt with by AdaFruit Library
    # def get_raw_data(self) -> bytes:
    def get_uid(self):
        return self.__uid
