from sensors.Sensor import Sensor
from sensors.SpecCoSensor import SpecCoSensor

sensor_mapping = {
    "spec_co_sensor": SpecCoSensor
}

def load_sensor_driver(sensor_name: str, device_path: str) -> Sensor:
  if sensor_name not in sensor_mapping:
    return None
  driver_class = sensor_mapping[sensor_name]
  return driver_class(uid=0, device=device_path)