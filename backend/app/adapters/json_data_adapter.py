"""
JSON Data Adapter - Persists readings to a JSON file.
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List

import aiofiles
import aiofiles.os

from app.core.config import settings
from app.core.models import SystemReading
from app.ports.data_port import DataPort

logger = logging.getLogger(__name__)


class JsonDataAdapter(DataPort):
    """
    Adapter for persisting readings to a JSON file.
    Uses append-mode for efficient writes.
    """
    
    def __init__(self, file_path: str = None):
        if file_path is None:
            data_dir = Path(settings.data_dir)
            file_path = str(data_dir / settings.readings_file)
        
        self.file_path = Path(file_path)
        self._lock = asyncio.Lock()
        self._buffer: List[SystemReading] = []
        self._buffer_size = 10  # Flush to disk every N readings
    
    async def _ensure_file_exists(self) -> None:
        """
        Ensure the data directory and file exist.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.file_path.exists():
            async with aiofiles.open(self.file_path, 'w') as f:
                await f.write('[]')
    
    async def append(self, reading: SystemReading) -> bool:
        """
        Append a reading to the JSON file.
        Uses buffering for efficiency.
        """
        try:
            async with self._lock:
                await self._ensure_file_exists()
                
                # Add to buffer
                self._buffer.append(reading)
                
                # Flush if buffer is full
                if len(self._buffer) >= self._buffer_size:
                    await self._flush_buffer()
                
                return True
                
        except Exception as e:
            logger.error(f"Error appending reading: {e}")
            return False
    
    async def _flush_buffer(self) -> None:
        """
        Flush the buffer to disk.
        """
        if not self._buffer:
            return
        
        try:
            # Read existing data
            async with aiofiles.open(self.file_path, 'r') as f:
                content = await f.read()
                data = json.loads(content) if content else []
            
            # Append buffered readings
            for reading in self._buffer:
                data.append(json.loads(reading.model_dump_json()))
            
            # Write back
            async with aiofiles.open(self.file_path, 'w') as f:
                await f.write(json.dumps(data, indent=2))
            
            self._buffer.clear()
            logger.debug(f"Flushed {len(self._buffer)} readings to disk")
            
        except Exception as e:
            logger.error(f"Error flushing buffer: {e}")
    
    async def flush(self) -> None:
        """
        Force flush the buffer to disk.
        """
        async with self._lock:
            await self._flush_buffer()
    
    async def get_all(self) -> List[SystemReading]:
        """
        Retrieve all readings from the JSON file.
        """
        try:
            await self._ensure_file_exists()
            
            async with aiofiles.open(self.file_path, 'r') as f:
                content = await f.read()
                data = json.loads(content) if content else []
            
            readings = [SystemReading(**item) for item in data]
            
            # Include buffer items not yet flushed
            readings.extend(self._buffer)
            
            return readings
            
        except Exception as e:
            logger.error(f"Error reading data: {e}")
            return []
    
    async def get_recent(self, count: int) -> List[SystemReading]:
        """
        Get the most recent N readings.
        """
        all_readings = await self.get_all()
        return all_readings[-count:] if len(all_readings) > count else all_readings
    
    async def clear(self) -> bool:
        """
        Clear all readings and create a new empty file.
        """
        try:
            async with self._lock:
                self._buffer.clear()
                async with aiofiles.open(self.file_path, 'w') as f:
                    await f.write('[]')
                logger.info("Cleared all readings")
                return True
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return False
    
    async def create_session_file(self) -> str:
        """
        Create a new session file with timestamp.
        Returns the new file path.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_path = self.file_path.parent / f"session_{timestamp}.json"
        self.file_path = new_path
        await self._ensure_file_exists()
        return str(new_path)
