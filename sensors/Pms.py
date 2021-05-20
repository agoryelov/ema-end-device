# inheritance library
# import abc
import Adafruit_DHT
# GPIO lib
import RPi.GPIO as GPIO           # import RPi.GPIO module

from sensors.SensorException import SensorReadError


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

class Pms(Sensor):
    """
        Credit for connect_to_port and get_raw_data goes to
        Noah MacRitchie (noah21mac@gmail.com) and Andrey Goryelov (andrey.goryelov@gmail.com)
    """

    # TODO: what is timeout ?
    # TODO: It is just a GPIO data in, not serial connection.
    # TODO: pass it in like : gpio_in = 1, named params
   
    def __init__(self, uid: int, device: str, timeout: int, baud_rate: int):
        self.__uid = uid
        self.__device = device
        self.__timeout = timeout
        self.__baud_rate = baud_rate
        self.__reading = ()


    # Sets the GPIO to be in input mode
    def connect_to_sensor(self) -> serial:
        f"""
        Connects the software to the sensor hardware.
        
        :return: {serial} 
        """
        try:
            ser = serial.Serial(self.__device, self.__baud_rate, timeout=self.__timeout, parity=serial.PARITY_NONE)
        except SerialException:
            Sensor.print_formatted_data({"error": "connecting to sensor"})
            exit(1)
        else:
            return ser



	# Get raw data
    def get_raw_data(self)-> float:
        start = time.time()

        sof_index = 0

        while True:
            elapsed = time.time() - start
            if elapsed > 5:
                raise ReadTimeoutError("PMS5003 Read Timeout: Could not find start of frame")

            sof = self._serial.read(1)
            if len(sof) == 0:
                raise SerialTimeoutError("PMS5003 Read Timeout: Failed to read start of frame byte")
            sof = ord(sof) if type(sof) is bytes else sof

            if sof == PMS5003_SOF[sof_index]:
                if sof_index == 0:
                    sof_index = 1
                elif sof_index == 1:
                    break
            else:
                sof_index = 0

        checksum = sum(PMS5003_SOF)

        data = bytearray(self._serial.read(2))  # Get frame length packet
        if len(data) != 2:
            raise SerialTimeoutError("PMS5003 Read Timeout: Could not find length packet")
        checksum += sum(data)
        frame_length = struct.unpack(">H", data)[0]

        raw_data = bytearray(self._serial.read(frame_length))
        print("frame_length:",frame_length)
        
        try:
            print("raw:",struct.unpack(">HHHHHHHHHHHHHH", raw_data))
        except:
            print("raw:","passed!")
            pass

        if len(raw_data) != frame_length:
            raise SerialTimeoutError("PMS5003 Read Timeout: Invalid frame length. Got {} bytes, expected {}.".format(len(raw_data), frame_length))

        data = PMS5003Data(raw_data)
        # Don't include the checksum bytes in the checksum calculation
        checksum += sum(raw_data[:-2])

        if checksum != data.checksum:
            raise ChecksumMismatchError("PMS5003 Checksum Mismatch {} != {}".format(checksum, data.checksum))

        return raw_data

    # Take reading from the sensor
    # (with retry, it's garunteed to get an output with up to 15 trials )
    def take_reading(self) -> int:
        try:
            self.__reading =  struct.unpack(">HHHHHHHHHHHHHH", self.get_raw_data())
            print("raw:", self.__reading)
        except:
            raise SensorReadError("cannot get a reading after 15 trials, please check wiring")

    def format_data(self) -> dict:
        reading = {
            ""
        }

if __name__ == "__main__":
	DEVICE = '/dev/ttyAMA0'
	TIMEOUT = 3
	BAUD_RATE = 9600
	PIN_ENABLE = 22
	PIN_RESET = 27
	
	UUID = 5002
	
	pms = Pms(UUID, DEVICE, TIMEOUT, BAUD_RATE)
	
	try:
		pms.take_reading()
	except SensorReadError:
		reading_data = {"error": "sensor error"}
	else:
		reading_data = pms.format_data()
	
	
	
