from sensors.Sensor import Sensor
from utils.config_loader import DeviceConfig
from utils.driver_loader import load_sensor_driver

CONFIG_PATH = "example_config.yaml"

def main():
    device_config = DeviceConfig(CONFIG_PATH)
    
    selected_sensors = device_config.get_sensors()
    
    loaded_drivers = dict()
    for sensor in selected_sensors:
        sensor_name, sensor_path = sensor['name'], sensor['path']

        print(f"Loading sensor {sensor_name} driver")
        driver : Sensor = load_sensor_driver(sensor_name, sensor_path)
        
        if driver is not None:
            loaded_drivers[sensor_name] = driver
            print(f'Successfully loaded {sensor_name} driver')
        else:
            print(f'Uanble to load {sensor_name} driver')
    
    for driver_name in loaded_drivers:
        sensor_driver : Sensor = loaded_drivers[driver_name]
        sensor_driver.connect_to_sensor()
        reading = sensor_driver.get_raw_data()
        print(f"Taking reading from {driver_name}: {reading}")

if __name__ == "__main__":
    main()