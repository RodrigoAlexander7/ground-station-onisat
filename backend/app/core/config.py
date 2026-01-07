"""
Application configuration using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Application
    app_name: str = "Wind Tunnel Data Acquisition System"
    debug: bool = True
    
    # Serial/Arduino Configuration
    serial_port: str = "/dev/ttyACM0"  # Linux default, use COM3 for Windows
    serial_baudrate: int = 9600
    serial_timeout: float = 1.0
    serial_retry_interval: float = 5.0  # Seconds between reconnection attempts
    use_mock_arduino: bool = False  # Use mock adapter for development
    
    # Data Configuration
    data_dir: str = "data"
    readings_file: str = "readings.json"
    reading_interval: float = 0.1  # Seconds between readings (100ms)
    
    # WebSocket Configuration
    ws_heartbeat_interval: float = 30.0  # Seconds
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
