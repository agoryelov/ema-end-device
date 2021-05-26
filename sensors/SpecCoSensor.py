from sensors.SpecDgs import SpecDgs
from sensors.SensorDataFormatter import SensorDataFormatter
from utils.unit_conversion.concentrations import ppb_to_ppm

# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021

TIMEOUT = 3
BAUD_RATE = 9600


class SpecCoSensor(SpecDgs, SensorDataFormatter):
    def __init__(self, uid: int, device: str, timeout: int = TIMEOUT, baud_rate: int = BAUD_RATE):
        super().__init__(uid, device, timeout, baud_rate)

    def format_data(self) -> dict:
        reading = {
            "uid": self.get_uid(),
            "serial_number": self.get_serial_number(),
            "CO": ppb_to_ppm(self.get_measurement()),
            "temperature": self.get_temperature(),
            "relative_humidity": self.get_relative_humidity(),
        }

        return reading
    
    def get_data(self) -> dict:
        reading_dict = {
            "uid": self.get_uid(),
            "serial_number": self.get_serial_number(),
            "co": ppb_to_ppm(self.get_measurement()),
            "temperature": self.get_temperature(),
            "humidity": self.get_relative_humidity(),
        }

        return reading_dict


