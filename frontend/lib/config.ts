/**
 * Environment configuration for the frontend
 */

export const config = {
  // WebSocket URL for backend connection
  wsUrl: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws',
  
  // REST API URL
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  
  // Chart configuration
  chart: {
    maxDataPoints: 100, // Maximum data points to display in charts
    animationDuration: 0, // Disable animation for real-time performance
  },
  
  // Update rates
  reconnectInterval: 3000, // ms between WebSocket reconnection attempts
};
