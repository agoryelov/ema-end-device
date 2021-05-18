import serial
from sensors import Sensor
from sensors.SensorException import SensorReadError
from unit_conversion import celsius_to_kelvin

# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021

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


class SpecDgs(Sensor):
    """
        Credit for connect_to_sensor and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """

    def __init__(self, uid: int, device: str, timeout: int, baud_rate: int):
        self.__uid = uid
        self.__device = device
        self.__timeout = timeout
        self.__baud_rate = baud_rate
        self.__reading = ()

    def connect_to_sensor(self) -> serial:
        # TODO error checking?
        ser = serial.Serial(self.__device, self.__baud_rate, timeout=self.__timeout, parity=serial.PARITY_NONE)
        return ser

    def get_raw_data(self) -> bytes:
        f"""
        Takes a reading from the sensor.
        
        :return: {bytes} 
        """
        start_reading = 'c'
        end_reading = 'R'

        ser = self.connect_to_sensor()
        ser.write(start_reading.encode())
        line = ser.readline()
        ser.write(end_reading.encode())

        return line

    def take_reading(self):
        """
        Decodes a raw data reading into a list.
        """

        self.__reading = tuple(self.get_raw_data().decode().split(","))

        if len(self.__reading) is not 11:
            raise SensorReadError("Error getting sensor reading")

    def get_uid(self):
        return self.__uid

    def get_serial_number(self) -> str:
        return str(self.__reading[DATA_INDICES["serial_number"]])

    def get_measurement(self) -> float:
        f"""
        Gets the measurement for which this sensor instance exists.
        
        e.g. if it's a CO sensor, the CO level is returned. 
        
        :return: {float} 
        """
        return float(self.__reading[DATA_INDICES["measurement"]])

    def get_temperature(self) -> float:
        f"""
        Gets the temperature reading of the sensor. Units in Kelvin

        :return: {float} 
        """
        temp_in_celsius = float(self.__reading[DATA_INDICES["temperature"]])

        return celsius_to_kelvin(temp_in_celsius)

    def get_relative_humidity(self) -> float:
        return float(self.__reading[DATA_INDICES["relative_humidity"]])

    def get_raw_sensor(self):
        return self.__reading[DATA_INDICES["raw_sensor"]]

    def get_temperature_digital(self) -> float:
        return float(self.__reading[DATA_INDICES["temp_digital"]])

    def get_relative_humidity_digital(self) -> float:
        return float(self.__reading[DATA_INDICES["rh_digital"]])

    def get_day(self):
        return self.__reading[DATA_INDICES["day"]]

    def get_hour(self) -> int:
        return int(self.__reading[DATA_INDICES["hour"]])

    def get_minute(self) -> int:
        return int(self.__reading[DATA_INDICES["minute"]])

    def get_second(self) -> int:
        return int(self.__reading[DATA_INDICES["second"]])