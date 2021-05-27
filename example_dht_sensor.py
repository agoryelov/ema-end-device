from sensors.Dht22 import Dht22 
from sensors.SensorException import SensorReadError

# uid: int, gpio_in: int, timeout : int, model : str 

UUID = 5001 # Some random fake uuid


def main():
    dht22_obj = Dht22(UUID)
    dht22_obj.connect_to_sensor()
    try:
        dht22_obj.take_reading()
    except SensorReadError:
        sensor_readings = {"error": "sensor error", "suggestions" : "check wiring" }
    except SensorUnitConversionError:
        sensor_readings = {"error": "sensor error", "suggestions" : "check original readings" }
    else:
        sensor_readings = dht22_obj.format_data()
        
    dht22_obj.print_formatted_data(sensor_readings)

if __name__ == '__main__':
    main()