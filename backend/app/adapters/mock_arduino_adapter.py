"""
Mock Arduino Adapter - Simulates sensor data for testing without hardware.
"""
import asyncio
import logging
import math
import random
from typing import Optional

from app.core.models import ArduinoReading
from app.ports.sensor_port import SensorPort

logger = logging.getLogger(__name__)


class MockArduinoAdapter(SensorPort):
    """
    Mock adapter that simulates Arduino sensor readings.
    Useful for testing and development without actual hardware.
    """
    
    def __init__(self):
        self._connected = False
        self._time = 0.0
        self._base_rpm = 1000.0
        self._base_lift = 5.0
    
    async def connect(self) -> bool:
        """
        Simulate connection (always succeeds).
        """
        await asyncio.sleep(0.1)  # Simulate connection delay
        self._connected = True
        logger.info("Mock Arduino connected")
        return True
    
    async def disconnect(self) -> None:
        """
        Simulate disconnection.
        """
        self._connected = False
        logger.info("Mock Arduino disconnected")
    
    async def read(self) -> Optional[ArduinoReading]:
        """
        Generate simulated sensor readings with realistic variations.
        """
        if not self._connected:
            return None
        
        # Increment time for smooth variations
        self._time += 0.1
        
        # Generate realistic-looking data with sine waves and noise
        rpm = self._base_rpm + 200 * math.sin(self._time * 0.5) + random.uniform(-50, 50)
        lift = self._base_lift + 2 * math.sin(self._time * 0.3) + random.uniform(-0.5, 0.5)
        
        # Ensure non-negative values
        rpm = max(0, rpm)
        
        return ArduinoReading(
            rpm=round(rpm, 2),
            lift_force=round(lift, 3),
            is_valid=True
        )
    
    def is_connected(self) -> bool:
        """
        Check if mock sensor is 'connected'.
        """
        return self._connected
    
    def set_base_values(self, rpm: float, lift: float) -> None:
        """
        Set base values for simulation (useful for testing different scenarios).
        """
        self._base_rpm = rpm
        self._base_lift = lift
