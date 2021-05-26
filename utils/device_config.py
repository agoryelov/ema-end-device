import yaml
import struct

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
    raise Exception("bad sensor name")

def number_to_bytes(number, data_type) -> bytearray:
  if data_type == 'int':
    return number.to_bytes(4, byteorder='big', signed=True)
  elif data_type == 'short':
    return number.to_bytes(2, byteorder='big', signed=True)
  elif data_type == 'byte':
    return number.to_bytes(1, byteorder='big', signed=True)
  elif data_type == 'float':
    return bytearray(struct.pack("f", number))
  elif data_type == 'double':
    return bytearray(struct.pack("d", number))
  else:
    return bytearray()

def reading_to_bytes(driver_values: dict, config_values: list):
  output = bytearray()
  
  for config_value in config_values:
    value = list(config_value.items())[0]
    name, data_type = value

    reading = driver_values[name]
    reading_bytes = number_to_bytes(reading, data_type)
    
    print(reading_bytes)
    print(len(reading_bytes))

    output.extend(reading_bytes)

  return(output)


def main():
  driver_values = { 'temperature': 21, 'humidity': 54, 'co': 553.2 }
  config_values = [{'temperature': 'int'}, {'humidity': 'short'}, {'co': 'float'}]


  reading_to_bytes(driver_values, config_values)


if __name__ == '__main__':
  main()