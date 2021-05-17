# Sensor interface
Copyright: Clinton Fernandes (2021)


A part of the BCIT Centre for Applied Research and Innovation EMA project.

This repo consists of an interface to define enviromental sensors so that consistency of output can be provided for downstream portions of the application.

In the examples folder is found a full implementation to a sensor: see examples/co_sensor.py.

## Using the interface

We have defined 3 levels in our hierarchy:
* Sensors
* Sensor manufacturers
* sensor model

e.g. SPEC-DGS (manufacturer) produces the CO sensor (sensor model).

### Sensors

SensorInterface (actually an abstract class) defines two methods to implement: connect_to_port() and get_raw_data()

**Note**: "raw data" is arbitrarily defined as the "first accessible" data from a sensor.
e.g. for a SPEC-DGS sensor that is accomplished by serial.readline() (see spec_dgs.py) and this puts out a host of information which may or may not be important.
By contrast, a DHT-22 sensor, when accessed via tha [AdaFruit library](https://pypi.org/project/adafruit-io/ "Adafuit python library"), outputs data that you are most likely directly interested in. i.e. the "raw data" is the processed data.

SensorInterface.print_formatted_data() implements a method that should be called by any sensor model to standardize output. It accepts a parameter supplied by format_data() (See Sensor manufacturers).

### Sensor manufacturers

Each Sensor manufacturer should define an abstract method, format_data(). A sensor model must implement that method to format data in an agreed-upon format. 

### Sensor model

Here you define any model-specific behaviour. For SPEC-DGS sensors this involves implementing format_data() (to be read by SensorInterface.print_formatted_data()

## Units

All measurements should be expressed in [SI units](https://en.wikipedia.org/wiki/International_System_of_Units). However, dimensionless quantities, like ppm (parts per million) are not SI and have no SI definition. For consistency, we've decided to standardize to ppm.

The included package, unit_conversion, provides convenient conversions. It is not exhaustive and should be updated as and when a conversion is needed. A different conversion package can be used if desired.

Future updates will have the unit_conversion package external. But there's no telling when that will occur.