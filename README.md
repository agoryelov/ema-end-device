# Sensor interface
Copyright: Clinton Fernandes (May 2021)


A part of the BCIT Centre for Applied Research and Innovation EMA project.

This repo consists of an interface to define environmental sensors so that consistency of output can be provided for 
downstream portions of the application.

 `example_co_sensor.py` is a full implementation of the sensor interface. 

## Installation

Clone/fork repo.

## Using the interface (overview)

We have defined three levels in our design hierarchy:
* Sensors
* Sensor manufacturers
* Sensor model

e.g. SPEC (sensor manufacturer) produces the [CO](https://www.digikey.ca/en/products/detail/spec-sensors-llc/968-034/6676880) 
sensor (sensor model).

### Sensors

`sensor.py` (an abstract base class) defines methods to implement:
* `connect_to_sensor()`
* `get_raw_data()`
* `get_data()`

It implements one method: `sensors/sensor.print_formatted_data()`. It can be called by any sensor model to
output data to console.  (See [Sensor manufacturers](#sensor-manufacturers)).

## `connect_to_sensor()` 

This method connects to the hardware.

## `get_raw_data()`

This method gets raw data from the sensor hardware.
***
**Note**: "raw data" is arbitrarily defined as the "first accessible" data from a sensor.
e.g. for a SPEC-DGS sensor that is accomplished by `serial.readline()` (see `sensors/SpecDgs.py`) and this 
puts out a host of information which may or may not be important.

By contrast, a DHT-22 sensor, when accessed via tha [AdaFruit library](https://pypi.org/project/adafruit-io/ "Adafuit python library"),
outputs data that you are most likely directly interested in. i.e. the "raw data" is the processed data.
***

## `get_data()`

This method is implemented by the sensor model class. It produces a dictionary of sensor data.


### Sensor manufacturers

Sensor manufacturers are the companies that put out different sensors. In our experience, all the sensors produced by
a sensor manufacturer have the same method to interact with the hardware, same output format, etc. 
As such, a sensor manufacturer can implement a lot of the logic to interact with a sensor. 

By contrast two different manufacturers may have wholly different ways to interact with the hardware.

e.g. 
* SPEC
* DHT
* Sensirion

**Note**: measurements should be expressed in SI units, so perform conversions here.
A class has been defined for this purpose; see [here](#units)

Manufacturers implement the Sensor interface.

example: `sensors/SpecDgs.py`

### Sensor model

Here you implement any model-specific behaviour.
  

For the purposes of consistency and precision, the following specifications are used for formatting outputs in `format_data()`:
* measurement types
  * use their full name e.g. 'temperature'
  * use only lower case e.g. 'temperature'
  * use underscores when joining words e.g. 'relative_humidity'
* chemicals
  * use [condensed structural formula]('https://en.wikipedia.org/wiki/Structural_formula#Condensed_formulas') 
    e.g. '(CH3)3CH' *not* 'C4H10'
  * use their symbol as identified in the [periodic table of elements]('https://en.wikipedia.org/wiki/Periodic_table')
    e.g. 'He' for Helium

e.g. `sensors/SpecCoSensor.py`

## Adding a new sensor to the system

We'll assume it's a new sensor from a new manufacturer.
If the manufacturer class has already been created then only [sensor class implementation](#2-implement-the-sensor-class) 
is necessary.

### 1. Implement a manufacturer class

This class must implement `sensors/Sensor.py`. 

Other properties/behaviours can be defined according to need.

Example: `sensors/SpecDgs.py`

### 2. Implement the sensor model class

This class extends the manufacturer class and implements `Sensor.get_data()`.

A convenience method, `Senors.print_formatted_data()` can take the return value from `Sensor.get_data()` and print it
out to console. 


Example: `sensors/SpecCoSensor.py`

### 3. Use your new class(es)

Example: `sensors/example_co_sensor.py`

## Known issues

### SPEC DGS

SPEC DGS sensors take a timeout property to read from. If the timeout is set insufficiently a reading will return 
malformed data.
A SensorReadError will be thrown in this case and final output will be an error message.

This issue may have been resolved in later code updates but has not been extensively tested.

### First-time run

The first time the script is run it results in a sensor read error. Subsequent executions function correctly.
* "first time" can mean
  * the first run after booting
  * the sensor has been removed and re-inserted
* "subsequent" can be up to 30 minutes (beyond that hasn't been tested)

## Related topics

### Python version

This portion of the project was designed and tested using Python v3.7.3

### Units

All measurements should be expressed in [SI units](https://en.wikipedia.org/wiki/International_System_of_Units). 
However, dimensionless quantities, like ppm (parts per million) are not SI and have no SI definition. For consistency, 
we've decided to *standardize to ppm*.

The included package, `utils/unit_conversion`, provides a convenient, though non-exhaustive library. 
It should be updated as and when a conversion is needed. A different conversion package can be used if desired.

Future updates will have the unit_conversion package external. But there's no telling when that will occur.
