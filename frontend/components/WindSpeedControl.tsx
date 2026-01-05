/**
 * WindSpeedControl - Input component for controlling wind speed
 */
'use client';

import React, { useState, useCallback, useEffect } from 'react';
import { useWindTunnelStore } from '@/lib/store';
import { useWebSocket } from '@/lib/useWebSocket';

export function WindSpeedControl() {
  const { windSpeedInput, setWindSpeedInput } = useWindTunnelStore();
  const { setWindSpeed, connectionStatus } = useWebSocket();
  
  const [localValue, setLocalValue] = useState(windSpeedInput);
  
  // Sync local value with store
  useEffect(() => {
    setLocalValue(windSpeedInput);
  }, [windSpeedInput]);
  
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value) || 0;
    setLocalValue(value);
  }, []);
  
  const handleSubmit = useCallback(() => {
    const value = Math.max(0, localValue);
    setWindSpeedInput(value);
    setWindSpeed(value);
  }, [localValue, setWindSpeedInput, setWindSpeed]);
  
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  }, [handleSubmit]);
  
  const handleSliderChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    setLocalValue(value);
    setWindSpeedInput(value);
    setWindSpeed(value);
  }, [setWindSpeedInput, setWindSpeed]);

  const isDisabled = connectionStatus !== 'connected';

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-lg border border-zinc-200 dark:border-zinc-800 p-4">
      <h3 className="text-lg font-semibold mb-4 text-zinc-900 dark:text-zinc-100">
        Control de Velocidad de Viento
      </h3>
      
      <div className="space-y-4">
        {/* Numeric Input */}
        <div className="flex items-center gap-3">
          <label className="text-sm text-zinc-600 dark:text-zinc-400 min-w-[100px]">
            Velocidad (m/s):
          </label>
          <input
            type="number"
            value={localValue}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onBlur={handleSubmit}
            disabled={isDisabled}
            min={0}
            max={50}
            step={0.1}
            className="flex-1 px-3 py-2 border border-zinc-300 dark:border-zinc-700 rounded-md 
                       bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100
                       focus:outline-none focus:ring-2 focus:ring-blue-500
                       disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            onClick={handleSubmit}
            disabled={isDisabled}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 
                       focus:outline-none focus:ring-2 focus:ring-blue-500
                       disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Aplicar
          </button>
        </div>
        
        {/* Slider */}
        <div className="space-y-2">
          <input
            type="range"
            value={localValue}
            onChange={handleSliderChange}
            disabled={isDisabled}
            min={0}
            max={50}
            step={0.5}
            className="w-full h-2 bg-zinc-200 dark:bg-zinc-700 rounded-lg appearance-none 
                       cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed
                       [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 
                       [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:bg-blue-600 
                       [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer"
          />
          <div className="flex justify-between text-xs text-zinc-500">
            <span>0 m/s</span>
            <span>25 m/s</span>
            <span>50 m/s</span>
          </div>
        </div>
        
        {/* Current Value Display */}
        <div className="text-center py-2 bg-zinc-100 dark:bg-zinc-800 rounded-md">
          <span className="text-2xl font-bold text-blue-600">
            {localValue.toFixed(1)}
          </span>
          <span className="text-sm text-zinc-500 ml-1">m/s</span>
        </div>
      </div>
    </div>
  );
}
