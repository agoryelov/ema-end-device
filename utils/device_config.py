import yaml
import struct

SHORT_BYTE_SIZE = 2
INT_BYTE_SIZE = 4

class DeviceConfig:
  def __init__(self, path):
    with open(path) as config_file:
      self.yaml_config = yaml.load(config_file, Loader=yaml.FullLoader)
  
  def get_attribute(self, attribute):
    return self.yaml_config[attribute]

  def get_device_id(self):
    return self.get_attribute('device_id')
  
  def get_sensors(self):
    return self.get_attribute('sensors')

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