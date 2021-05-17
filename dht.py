from sensors import dht22 


# uid: int, gpio_in: int, timeout : int, model : str 

GPIO_IN = 4 # DHT22
# TIMEOUT = 10
# 
MODEL = 'DHT22' # Not needed

UUID = 5001 # Some random fake uuid


def main():
    dht22_obj = dht22(UUID, GPIO_IN, MODEL)
    dht22_obj.take_reading()
    dht22_obj.print_data()

if __name__ == '__main__':
    main()