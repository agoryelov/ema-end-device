import abc


# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021

class SensorDataFormatter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'format_data') and
                callable(subclass.format_data) or
                NotImplemented)

    @abc.abstractmethod
    def format_data(self) -> dict:
        f"""
           Provides formatted sensor data for output.

           Specifications:
           - key names must be fully spelled out. e.g. 'carbon_monoxide', 'relative_humidity'

           :return: {dict} 
           """
        raise NotImplementedError
