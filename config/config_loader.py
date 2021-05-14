import yaml

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