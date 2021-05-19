import abc
import json


# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021

class Sensor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'connect_to_sensor') and
                callable(subclass.connect_to_sensor) and
                hasattr(subclass, 'get_raw_data') and
                callable(subclass.get_raw_data) or
                NotImplemented)

    @abc.abstractmethod
    def connect_to_sensor(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_raw_data(self) -> bytes:
        raise NotImplementedError

    @staticmethod
    def print_formatted_data(data: dict):
        f"""
        Outputs formatted sensor data as a JSON.
        
        :param data: {dict} 
        """
        json_data = json.dumps(data)

        print(json_data)
