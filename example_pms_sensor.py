from sensors.Pms import Pms

def main():
	DEVICE = '/dev/ttyAMA0'	
	UUID = 5002
	
	pms = Pms(UUID, DEVICE)
	
	try:
		pms.take_reading()
	except SensorReadError:
		reading_data = {"error": "sensor error"}
	else:
		reading_data = pms.format_data()
	
	pms.print_formatted_data(reading_data)

if __name__ == "__main__":
    main()
