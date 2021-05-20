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
    
    "gt0.3μm" : 6,
    "gt0.5μm" : 7,
    "gt1.0μm" : 8,
    "gt2.5μm" : 9,
    "gt5.0μm" : 10,
    "gt10μm" : 11,
    }


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

    def get_pm_1_raw(self)->float:
        return self.__reading[DATA_INDICES['PM1.0']]
    
    def get_pm_2_5_raw(self)->float:
        return self.__reading[DATA_INDICES['PM2.5']]
    
    def get_pm_10_raw(self)->float:
        return self.__reading[DATA_INDICES['PM2.5']]
    
    def get_pm_1(self)->float:
        return μgm3_to_gpl(self.__reading[DATA_INDICES['PM1.0']])
    
    def get_pm_2_5(self)->float:
        return μgm3_to_gpl(self.__reading[DATA_INDICES['PM2.5']])
    
    def get_pm_10(self)->float:
        return μgm3_to_gpl(self.__reading[DATA_INDICES['PM2.5']])
    
    
    
    #greater than 
    def get_gt_0_3_raw(self)->float:
        return self.__reading[DATA_INDICES['gt0.3μm']]
    
    def get_gt_0_5_raw(self)->float:
        return self.__reading[DATA_INDICES['gt0.5μm']]
    
    def get_gt_1_raw(self)->float:
        return self.__reading[DATA_INDICES['gt1.0μm']]
    
    def get_gt_2_5_raw(self)->float:
        return self.__reading[DATA_INDICES['gt2.5μm']]

    def get_gt_5_raw(self)->float:
        return self.__reading[DATA_INDICES['gt5.0μm']]
    
    def get_gt_10_raw(self)->float:
        return self.__reading[DATA_INDICES['gt10μm']]
    
    # processed
    def get_gt_0_3(self)->float:
        return pms_gt_output_to_si(self.__reading[DATA_INDICES['gt0.3μm']])
    
    def get_gt_0_5(self)->float:
        return pms_gt_output_to_si(self.__reading[DATA_INDICES['gt0.5μm']])
    
    def get_gt_1(self)->float:
        return pms_gt_output_to_si(self.__reading[DATA_INDICES['gt1.0μm']])
    
    def get_gt_2_5(self)->float:
        return pms_gt_output_to_si(self.__reading[DATA_INDICES['gt2.5μm']])

    def get_gt_5(self)->float:
        return pms_gt_output_to_si(self.__reading[DATA_INDICES['gt5.0μm']])
    
    def get_gt_10(self)->float:
        return pms_gt_output_to_si(self.__reading[DATA_INDICES['gt10μm']])
    
    

	# Get raw data
    def get_raw_data(self)-> float:
        
        ser = self.connect_to_sensor()
        
        start = time.time()

        sof_index = 0

        while True:
            elapsed = time.time() - start
            if elapsed > 5:
                raise ReadTimeoutError("PMS5003 Read Timeout: Could not find start of frame")

            sof = ser.read(1)
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

        data = bytearray(ser.read(2))  # Get frame length packet
        if len(data) != 2:
            raise SerialTimeoutError("PMS5003 Read Timeout: Could not find length packet")
        checksum += sum(data)
        frame_length = struct.unpack(">H", data)[0]

        raw_data = bytearray(ser.read(frame_length))
        print("frame_length:",frame_length)
    

        if len(raw_data) != frame_length:
            raise SerialTimeoutError("PMS5003 Read Timeout: Invalid frame length. Got {} bytes, expected {}.".format(len(raw_data), frame_length))


        return raw_data

    # Take reading from the sensor
    # (with retry, it's garunteed to get an output with up to 15 trials )
    def take_reading(self) -> int:
        print("take_reading()")
        print(self.get_raw_data())
        try:
            self.__reading =  struct.unpack(">HHHHHHHHHHHHHH", self.get_raw_data())
            print("reading:", self.__reading)
        except:
            raise SensorReadError("cannot get a reading after 15 trials, please check wiring")

    def format_data(self) -> dict:
        reading = {
           # "PM1.0 ug/m3:" : self.get_pm_1_raw(),
           # "PM2.5 ug/m3:" : self.get_pm_2_5_raw(),
           # "PM10  ug/m3" : self.get_pm_10_raw(),
            
            'PM1.0': self.get_pm_1()  ,
            'PM2.5': self.get_pm_2_5(),
            'PM10:' : self.get_pm_10(),
            
            '> 0.3 um/L' : self.get_gt_0_3(),
            '> 0.5 um/L' : self.get_gt_0_5(),
            '> 1.0 um/L' : self.get_gt_1(),
            '> 2.5 um/L' : self.get_gt_2_5(),
            '> 5.0 um/L' : self.get_gt_5(),
            '> 10 um/L' :  self.get_gt_10(),
        }
        return reading
        

#PM1.0 ug/m3 (ultrafine particles):                             {}
#PM2.5 ug/m3 (combustion particles, organic compounds, metals): {}
#PM10 ug/m3  (dust, pollen, mould spores):                      {}
#PM1.0 ug/m3 (atmos env):                                       {}
#PM2.5 ug/m3 (atmos env):                                       {}
#PM10 ug/m3 (atmos env):                                        {}
#>0.3um in 0.1L air:                                            {}
#>0.5um in 0.1L air:                                            {}
#>1.0um in 0.1L air:                                            {}
#>2.5um in 0.1L air:                                            {}
#>5.0um in 0.1L air:                                            {}
#>10um in 0.1L air:                                             {}
