# inheritance library
# import abc
import Adafruit_DHT
# GPIO lib
import RPi.GPIO as GPIO           # import RPi.GPIO module

import serial

import struct

from sensors.SensorException import SensorReadError

import time

# SensorInterface(Top Hierarchy)
# Author     : clintonbf
# Repository :   https://github.com/clintonbf/sensor_interface/blob/master/sensors/SensorInterface.py
from sensors.Sensor import Sensor

# unit conversion function
# Author     : clintonbf
# Repository : https://github.com/clintonbf/sensor_interface/tree/master/unit_conversion
from utils.unit_conversion.concentrations import μgm3_to_gpl
from utils.unit_conversion.concentrations import pms_gt_output_to_si


DATA_INDICES = {
    "PM1.0": 0,
    "PM2.5": 1,
    "PM10" : 2,
    
    "gt0.3um" : 6,
    "gt0.5um" : 7,
    "gt1.0um" : 8,
    "gt2.5um" : 9,
    "gt5.0um" : 10,
    "gt10um" : 11,
    }

# Start of file flag
PMS5003_SOF = bytearray(b'\x42\x4d')


class ChecksumMismatchError(RuntimeError):
    pass


class ReadTimeoutError(RuntimeError):
    pass


class SerialTimeoutError(RuntimeError):
    pass

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

    def get_pm_raw(self, size) -> float:
        return self.__reading[DATA_INDICES[f'PM{size}']]

    def get_pm(self, size) -> float:
        return μgm3_to_gpl(self.__reading[DATA_INDICES[f'PM{size}']])
    
    def get_particles_gt_raw(self, micrometers):
        return self.__reading[DATA_INDICES[f'gt{micrometers}um']]
    
    def get_particles_gt(self, micrometers):
        return pms_gt_output_to_si(self.__reading[DATA_INDICES[f'g{micrometers}um']])
    
    # Get raw data
    def get_raw_data(self)-> float:
        
        ser = self.connect_to_sensor()
        
        start = time.time()

        start_of_file_index = 0

        while True:
            elapsed = time.time() - start
            if elapsed > 5:
                raise ReadTimeoutError("PMS5003 Read Timeout: Could not find start of frame")

            start_of_file = ser.read(1)
            if len(start_of_file) == 0:
                raise SerialTimeoutError("PMS5003 Read Timeout: Failed to read start of frame byte")
            start_of_file = ord(start_of_file) if type(start_of_file) is bytes else start_of_file

            if start_of_file == PMS5003_SOF[start_of_file_index]:
                if start_of_file_index == 0:
                    start_of_file_index = 1
                elif start_of_file_index == 1:
                    break
            else:
                start_of_file_index = 0

        checksum = sum(PMS5003_SOF)

        data = bytearray(ser.read(2))  # Get frame length packet
        if len(data) != 2:
            raise SerialTimeoutError("PMS5003 Read Timeout: Could not find length packet")
        checksum += sum(data)
        frame_length = struct.unpack(">H", data)[0]

        raw_data = bytearray(ser.read(frame_length))
  
        if len(raw_data) != frame_length:
            raise SerialTimeoutError("PMS5003 Read Timeout: Invalid frame length. Got {} bytes, expected {}.".format(len(raw_data), frame_length))

        return raw_data

    def take_reading(self) -> int:
        try:
            self.__reading =  struct.unpack(">HHHHHHHHHHHHHH", self.get_raw_data())
        except:
            raise SensorReadError("cannot get a reading after 15 trials, please check wiring")

    def get_data(self) -> dict:
        self.take_reading()
        reading = {            
            'PM1.0': self.get_pm('1.0'),
            'PM2.5': self.get_pm('2.5'),
            'PM10:' : self.get_pm('10'),
            
            'gt_300_nm_ppL' : self.get_particles_gt(micrometers='0.3'),
            'gt_500_nm_ppL' : self.get_particles_gt(micrometers='0.5'),
            'gt_1000_nm_ppL' : self.get_particles_gt(micrometers='1.0'),
            'gt_2500_nm_ppL' : self.get_particles_gt(micrometers='2.5'),
            'gt_5000_nm_ppL' : self.get_particles_gt(micrometers='5.0'),
            'gt_10_um_ppL' :  self.get_particles_gt(micrometers='10'),
        }
        return reading
