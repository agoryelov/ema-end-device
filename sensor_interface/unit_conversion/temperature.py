# Copyright Clinton Fernandes (clint.fernandes@gmail.com) 2021

def celsius_to_kelvin(temp_in_celsius: float) -> float:
    f"""
    Converts a temperature in degrees Celsius/Centigrade to degrees Kelvin.
    
    Does not account for decimal precision (if such a thing is a concern).
    
    :param temp_in_celsius: {float}  
    :return: {float}
    """
    conversion = 273.15
    absolute_zero = -273.15

    if temp_in_celsius < absolute_zero:
        raise ValueError("Temperature cannot be below absolute zero")
    else:
        return temp_in_celsius + conversion


def fahrenheit_to_kelvin(temp_in_fahrenheit: float) -> float:
    f"""
    Converts a temperature in degrees Fahrenheit to degrees Kelvin.
    
    Does not account for decimal precision (if such a thing is a concern).
    :param temp_in_fahrenheit: {float}
    :return: {float}
    """

    absolute_zero = -459.67

    if temp_in_fahrenheit < absolute_zero:
        raise ValueError("Temperature cannot be below absolute zero")
    else:
        return (temp_in_fahrenheit - 32) * 5/9 + 273.15