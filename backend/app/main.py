"""
Wind Tunnel Data Acquisition System - Main Application.
FastAPI application with WebSocket support for real-time monitoring.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.adapters.mock_arduino_adapter import MockArduinoAdapter
from app.adapters.arduino_adapter import ArduinoAdapter
from app.adapters.json_data_adapter import JsonDataAdapter
from app.services.measurement_manager import MeasurementManager
from app.api.websocket import router as websocket_router
from app.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Determine which adapter to use based on environment
USE_MOCK = os.getenv("USE_MOCK_ARDUINO", "true").lower() == "true"

# Initialize adapters
if USE_MOCK:
    logger.info("Using Mock Arduino adapter (set USE_MOCK_ARDUINO=false to use real Arduino)")
    sensor_adapter = MockArduinoAdapter()
else:
    logger.info(f"Using real Arduino adapter on {settings.serial_port}")
    sensor_adapter = ArduinoAdapter()

data_adapter = JsonDataAdapter()

# Initialize measurement manager (global for access from routes)
measurement_manager = MeasurementManager(
    sensor=sensor_adapter,
    data_store=data_adapter
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Starts/stops the measurement manager with the application.
    """
    logger.info("Starting Wind Tunnel Data Acquisition System...")
    
    # Start the measurement manager
    await measurement_manager.start()
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down...")
    await measurement_manager.stop()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Real-time data acquisition system for wind tunnel experiments",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(websocket_router)
app.include_router(api_router)


@app.get("/")
async def root():
    """
    Root endpoint with basic info.
    """
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
