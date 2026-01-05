/**
 * StatusPanel - Shows connection and system status
 */
'use client';

import React from 'react';
import { useWindTunnelStore } from '@/lib/store';
import { useWebSocket } from '@/lib/useWebSocket';

export function StatusPanel() {
  const { systemStatus, readings, isRecording } = useWindTunnelStore();
  const { connectionStatus, startRecording, stopRecording, clearReadings } = useWebSocket();

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'bg-green-500';
      case 'connecting':
        return 'bg-yellow-500 animate-pulse';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-zinc-500';
    }
  };

  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Conectado';
      case 'connecting':
        return 'Conectando...';
      case 'error':
        return 'Error';
      default:
        return 'Desconectado';
    }
  };

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-lg border border-zinc-200 dark:border-zinc-800 p-4">
      <h3 className="text-lg font-semibold mb-4 text-zinc-900 dark:text-zinc-100">
        Estado del Sistema
      </h3>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        {/* WebSocket Status */}
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${getStatusColor()}`} />
          <span className="text-sm text-zinc-600 dark:text-zinc-400">
            WebSocket: {getStatusText()}
          </span>
        </div>
        
        {/* Arduino Status */}
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${
            systemStatus?.arduino_connected ? 'bg-green-500' : 'bg-red-500'
          }`} />
          <span className="text-sm text-zinc-600 dark:text-zinc-400">
            Arduino: {systemStatus?.arduino_connected ? 'Conectado' : 'Desconectado'}
          </span>
        </div>
        
        {/* Readings Count */}
        <div className="text-sm text-zinc-600 dark:text-zinc-400">
          Lecturas en buffer: <span className="font-mono">{readings.length}</span>
        </div>
        
        {/* Recording Status */}
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${
            isRecording ? 'bg-red-500 animate-pulse' : 'bg-zinc-500'
          }`} />
          <span className="text-sm text-zinc-600 dark:text-zinc-400">
            {isRecording ? 'Grabando...' : 'Sin grabar'}
          </span>
        </div>
      </div>
      
      {/* Control Buttons */}
      <div className="flex gap-2">
        {!isRecording ? (
          <button
            onClick={startRecording}
            disabled={connectionStatus !== 'connected'}
            className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 
                       disabled:opacity-50 disabled:cursor-not-allowed transition-colors
                       flex items-center justify-center gap-2"
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <circle cx="10" cy="10" r="6" />
            </svg>
            Iniciar Grabación
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 
                       transition-colors flex items-center justify-center gap-2"
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <rect x="6" y="6" width="8" height="8" />
            </svg>
            Detener Grabación
          </button>
        )}
        
        <button
          onClick={clearReadings}
          disabled={connectionStatus !== 'connected' || isRecording}
          className="px-4 py-2 bg-zinc-600 text-white rounded-md hover:bg-zinc-700 
                     disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Limpiar
        </button>
      </div>
    </div>
  );
}
