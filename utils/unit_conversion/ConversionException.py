# Raised when failed to convert 
class SensorUnitConversionError(RuntimeError):
    def __init__(self,message):
        pass
    @property
    def message(self):
        return self.__message
    def get_message(self):
        return self.__message
