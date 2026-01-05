"""
Abstract port for data persistence.
"""
from abc import ABC, abstractmethod
from typing import List
from app.core.models import SystemReading


class DataPort(ABC):
    """
    Abstract interface for data persistence.
    Implementations can be JSON file, Database, etc.
    """
    
    @abstractmethod
    async def append(self, reading: SystemReading) -> bool:
        """
        Append a new reading to the storage.
        Returns True if successful.
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[SystemReading]:
        """
        Retrieve all readings from storage.
        """
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """
        Clear all readings from storage.
        """
        pass
    
    @abstractmethod
    async def get_recent(self, count: int) -> List[SystemReading]:
        """
        Get the most recent N readings.
        """
        pass
