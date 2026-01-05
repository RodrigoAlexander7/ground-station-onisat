"""
API dependencies for dependency injection.
"""
from typing import Generator

from app.services.measurement_manager import MeasurementManager


def get_measurement_manager() -> MeasurementManager:
    """
    Dependency to get the measurement manager instance.
    """
    from app.main import measurement_manager
    return measurement_manager
