from sensors.Dht22 import Dht22 


# uid: int, gpio_in: int, timeout : int, model : str 

GPIO_IN = 4 # DHT22 gpio data in
MODEL = 'DHT22' # Not needed
UUID = 5001 # Some random fake uuid


def main():
    dht22_obj = Dht22(UUID, GPIO_IN, MODEL)
    dht22_obj.connect_to_sensor()
    try:
        dht22_obj.take_reading()
    except SensorReadError:
        sensor_readings = {"error": "sensor error"}
    else:
        sensor_readings = dht22_obj.format_data()
        
    dht22_obj.print_formatted_data(sensor_readings)

if __name__ == '__main__':
    main()