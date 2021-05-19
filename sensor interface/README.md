# Sensor interface
Copyright: Clinton Fernandes (May 2021)


A part of the BCIT Centre for Applied Research and Innovation EMA project.

This repo consists of an interface to define enviromental sensors so that consistency of output can be provided for 
downstream portions of the application.

In the examples folder is found a full implementation to a sensor: see [examples/co_sensor.py](./examples/co_sensor.py)

## Installation

If pulling directly from the repo the package folders must be present in the same folder as sensor implementations.
In the directory structure present in the repo, this means that sensors/ and unit_conversion/ must be brought 
into examples/.

On a *ix system this is mostly easily done via symlinks. On Windows the files must be copied into the working directory.

(May 2021): A future goal is to have the packages in pypi or something similar so that they can be installed in the same
place as other imported packages (sys.path).

## Using the interface (overview)

We have defined 3 levels in our hierarchy:
* Sensors
* Sensor manufacturers
* Sensor model

e.g. SPEC (sensor manufacturer) produces the [CO](https://www.digikey.ca/en/products/detail/spec-sensors-llc/968-034/6676880) 
sensor (sensor model).

### Sensors

sensor.py (an abstract base class) defines two methods to implement: connect_to_sensor() and get_raw_data()

**Note**: "raw data" is arbitrarily defined as the "first accessible" data from a sensor.
e.g. for a SPEC-DGS sensor that is accomplished by serial.readline() (see [SpecDgs.py](sensors/SpecDgs.py)) and this 
puts out a host of information which may or may not be important.
By contrast, a DHT-22 sensor, when accessed via tha [AdaFruit library](https://pypi.org/project/adafruit-io/ "Adafuit python library"),
outputs data that you are most likely directly interested in. i.e. the "raw data" is the processed data.

sensor.print_formatted_data() implements a method that should be called by any sensor model to standardize output. 
It accepts a parameter supplied by format_data() (See [Sensor manufacturers](#sensor-manufacturers)).

### Sensor manufacturers

**Note**: measurements should be expressed in SI units, so perform conversions in this implementation.
A class has been defined for this purpose; see [here](#units)

### Sensor model

Here you define any model-specific behaviour. For SPEC-DGS sensors this involves implementing format_data() 
(to be supplied to sensor.print_formatted_data()

Each Sensor manufacturer must implement [SensorDataFormatter.format_data()](sensors/SensorDataFormatter.py) to format 
data in a consistent format.


## Adding a new sensor to the system

We'll assume it's a new sensor from a new manufacturer.
If the manufacturer class has already been created then only [sensor class implementation](#2-implement-the-sensor-class) 
is necessary.

### 1. Implement a manufacturer class

This class must implement [Sensor.py](sensors/Sensor.py) 

Other properties/behaviours can be defined according to need.

Example: [SpecDgs.py](sensors/SpecDgs.py)

### 2. Implement the sensor class

This class extends the manufacturer class & must implement [SensorDataFormatter.py](sensors/SensorDataFormatter.py)

Unless you have a very good reason you should use `Sensor.print_formatted_data()` to output your data. This will keep
things nice and consistent.

Example: [SpecCoSensor.py](sensors/SpecCoSensor.py)


### 3. Use your new class(es)

Example: [co_sensor.py](./examples/co_sensor.py)

## Known issues

### SPEC DGS

SPEC DGS sensors take a timeout property to read from. If the timeout is set insufficiently then a reading will return 
malformed data.
A SensorReadError will be thrown in this case and final output will be an error message

### Python package locations

For reasons I don't understand (yet) the sensors/ and unit_conversion/ packages must be in the same directory as the
harnessing script (co_sensor.py in the examples). See [Installation](#installation)

### First-time run

The first time the script is run it results in a sensor read error. Subsequent executions function correctly.
* "first time" can mean
  * the first run after booting
  * the sensor has been removed and re-inserted
* "subsequent" can be up to 10 minutes (beyond that hasn't been tested)

## Related topics

### Units

All measurements should be expressed in [SI units](https://en.wikipedia.org/wiki/International_System_of_Units). 
However, dimensionless quantities, like ppm (parts per million) are not SI and have no SI definition. For consistency, 
we've decided to *standardize to ppm*.

The included package, [unit_conversion](./unit_conversion), provides a convenient, though non-exhaustive library. 
It should be updated as and when a conversion is needed. A different conversion package can be used if desired.

Future updates will have the unit_conversion package external. But there's no telling when that will occur.
