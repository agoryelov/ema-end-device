from sensors.SpecCoSensor import SpecCoSensor
from sensors.SensorException import SensorReadError

# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021

DEVICE = '/dev/ttyUSB0'
UUID = 5000


def main():
    co = SpecCoSensor(UUID, DEVICE)

    try:
        co.take_reading()
    except SensorReadError:
        reading_data = {"error": "sensor error"}
    else:
        reading_data = co.format_data()

    co.print_formatted_data(reading_data)


if __name__ == '__main__':
    main()
