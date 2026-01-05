"""
Abstract port for sensor data input.
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.core.models import ArduinoReading


class SensorPort(ABC):
    """
    Abstract interface for sensor data sources.
    Implementations can be Arduino via Serial, Mock sensors, etc.
    """
    
    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to the sensor.
        Returns True if successful.
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """
        Close the connection to the sensor.
        """
        pass
    
    @abstractmethod
    async def read(self) -> Optional[ArduinoReading]:
        """
        Read data from the sensor.
        Returns None if reading fails.
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if the sensor is currently connected.
        """
        pass
