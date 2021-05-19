from sensors import Dht22 


# uid: int, gpio_in: int, timeout : int, model : str 

GPIO_IN = 5 # DHT22 gpio data in
MODEL = 'DHT22' # Not needed
UUID = 5001 # Some random fake uuid


def main():
    dht22_obj = Dht22(UUID, GPIO_IN, MODEL)
    dht22_obj.connect_to_sensor()
    dht22_obj.take_reading()
    sensor_readings = dht22_obj.format_data()
    dht22_obj.print_formatted_data(sensor_readings)

if __name__ == '__main__':
    main()