from sensors.spec_dgs import SPEC_DGS
from sensors.sensor_data_formatter import SENSOR_DATA_FORMATTER
from unit_conversion import ppb_to_ppm


# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021


class SPEC_CO_SENSOR(SPEC_DGS, SENSOR_DATA_FORMATTER):
    def __init__(self, uid: int, device: str, timeout: int, baud_rate: int):
        super().__init__(uid, device, timeout, baud_rate)

    def format_data(self) -> dict:
        reading = {
            "uid": self.get_uid(),
            "serial_number": self.get_serial_number(),
            "carbon_monoxide": ppb_to_ppm(self.get_measurement()),
            "temperature": self.get_temperature(),
            "relative_humidity": self.get_relative_humidity(),
        }

        return reading
