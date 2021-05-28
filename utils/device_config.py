import yaml
import struct

SHORT_BYTE_SIZE = 2
INT_BYTE_SIZE = 4

class DeviceConfig:
    def __init__(self, file_addr):
        """
        A Python class to read, parse and set end device
        configurations from a yaml file
        :param file_addr: address of the configuration file
        """
        self.__file = file_addr
        self.__configs = {}
        self.parseFile(self.__file)

    def parseFile(self, file_addr):
        """
        parses the given config file, converts the YAML scalar values
        to the Python dictionary format and saves it as self.configs
        :param file_addr: address of the configuration file
        """
        self.__file = file_addr
        with open(file_addr) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to the Python dictionary format
            self.__configs = yaml.load(file, Loader=yaml.FullLoader)

    def get_file(self):
        """Get the current file address"""
        return self.__file

    def set_file(self, file_addr):
        """Update the current file address and parse configs
        :param file_addr: address of a new config file to be set
        """
        self.parseFile(file_addr)

    def get_configs(self):
        """Get the parsed configs dictionary"""
        return self.__configs

    def get_config_keys(self):
        """Get a list of all the keys in current
        config dictionary"""
        return self.__configs.keys()

    def get_config_value(self, config_key):
        """
        Get the value of a given configuration_key
        :param config_key: Name of the configuration
        """
        return self.__configs[config_key]
    
    def get_sensors(self):
      return self.__configs['sensors']
    
    def get_values(self, sensor_name):
      sensors = self.get_sensors()
      for sensor in sensors:
        if sensor['name'] is sensor_name:
          return sensor['values']
      raise ValueError("Invalid sensor name")

def number_to_bytes(number, data_type) -> bytearray:
  if data_type == 'int':
    return int(number).to_bytes(INT_BYTE_SIZE, byteorder='big', signed=True)
  elif data_type == 'short':
    return int(number).to_bytes(SHORT_BYTE_SIZE, byteorder='big', signed=True)
  elif data_type == 'byte':
    return int(number).to_bytes(1, byteorder='big', signed=True)
  elif data_type == 'float':
    return bytearray(struct.pack("f", float(number)))
  elif data_type == 'double':
    return bytearray(struct.pack("d", float(number)))
  else:
    return bytearray()

def reading_to_bytes(driver_values: dict, config_values: list) -> bytearray:
  output = bytearray()
  
  for config_value in config_values:
    value = list(config_value.items())[0]
    name, data_type = value

    reading = driver_values[name]
    reading_bytes = number_to_bytes(reading, data_type)

    output.extend(reading_bytes)

  return output