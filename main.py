from collections import OrderedDict
import time
from transmit.utils import handshake, sleep_and_reconnect
from transmit.connectClient import Connection
from transmit.accessnet import Finder
from utils.device_config import reading_to_bytes
from sensors.Sensor import Sensor
from utils.device_config import DeviceConfig
from utils.driver_loader import load_sensor_driver

CONFIG_PATH = "example_config.yaml"

def load_drivers(selected_sensors) -> OrderedDict:
    loaded_drivers = OrderedDict()
    for sensor in selected_sensors:
        sensor_name, sensor_path = sensor['name'], sensor['path']

        print(f"Loading sensor {sensor_name} driver")
        driver : Sensor = load_sensor_driver(sensor_name, sensor_path)
        
        if driver is not None:
            loaded_drivers[sensor_name] = driver
            print(f'Loaded {sensor_name} driver')
        else:
            print(f'Uanble to load {sensor_name} driver')
    return loaded_drivers

def get_packed_readings(loaded_drivers, device_config) -> bytearray:
    packed_readings = bytearray()
    for sensor_name in loaded_drivers:
        sensor_driver : Sensor = loaded_drivers[sensor_name]

        print(f'Connecting to sensor {sensor_name}')
        connected = sensor_driver.connect_to_sensor()
        
        if connected:
            driver_values = sensor_driver.get_data()
            config_values = device_config.get_values(sensor_name)
            print(f"Taking a reading from {sensor_name}: {driver_values}")
            
            sensor_reading = reading_to_bytes(driver_values, config_values)
            print(f'Packed binary reading from {sensor_name}: {sensor_reading}')
            packed_readings.extend(sensor_reading)
    
    return packed_readings

def main():
    # setup configurations
    configs = DeviceConfig(CONFIG_PATH)
    
    selected_sensors = configs.get_sensors()
    loaded_drivers = load_drivers(selected_sensors)

    medium = configs.get_config_value("communication_medium")

    # connect to wifi if necessary
    # if medium == "wifi":
    #     ssid = configs.get_config_value("access_point_ssid")
    #     p_key = configs.get_config_value("access_point_password")
    #     if p_key == "none":
    #         p_key = None
    #     wap = Finder(server_name=ssid, password=p_key, interface="wlx000f6001ea46")
    #     wap.connection()

    # setup socket connection. default is AF_UNIX, you can set bluetooth too
    edge_addr = configs.get_config_value("edge_device_address")
    edge_port = configs.get_config_value("edge_device_port")
    socket = Connection()
    socket.connect_to_host(edge_addr, int(edge_port))

    # seconds between each message sent after handshake
    msg_rate = int(configs.get_config_value("transmission_rate"))

    # initially local_device_id is 0
    local_device_id = 0

    # you get a new id for future connections
    local_device_id = handshake(socket, local_device_id)

    while True:
        packed_readings = get_packed_readings(loaded_drivers, configs)
        socket.s_send(packed_readings)
        if bool(configs.get_config_value("keep_alive")):
            time.sleep(msg_rate)
        else:
            socket = sleep_and_reconnect(msg_rate, socket, edge_addr, edge_port)
            local_device_id = handshake(socket, local_device_id)


if __name__ == "__main__":
    main()