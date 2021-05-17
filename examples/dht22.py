from sensors import dht22 


# uid: int, gpio_in: int, timeout : int, model : str 

GPIO_IN = 4 # DHT22
TIMEOUT = 10
MODEL = 'DHT22' # Not needed

UUID = 5001 # Some random fake uuid


def main():
    dht22 = dht22(UUID, GPIO_IN, TIMEOUT, MODEL)
    dht22.take_reading()
    dht22.print_data()

if __name__ == '__main__':
    main()