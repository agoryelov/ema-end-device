from sensors import spec_co_sensor

# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021


DEVICE = '/dev/ttyUSB0'
TIMEOUT = 10
BAUD_RATE = 9600

UUID = 5000


def main():
    co = spec_co_sensor(UUID, DEVICE, TIMEOUT, BAUD_RATE)
    co.take_reading()

    reading_data = co.format_data()
    co.print_formatted_data(reading_data)


if __name__ == '__main__':
    main()