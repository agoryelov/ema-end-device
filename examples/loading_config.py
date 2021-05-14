from ..config_loader import DeviceConfig

def main():
  device_config = DeviceConfig('example_config.yaml')
  print(device_config.get_device_id())

if __name__ == "__main__":
  main()