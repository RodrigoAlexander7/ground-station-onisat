/**
 * ChartModule - Reusable chart component using Recharts
 * Supports any X and Y key from the data for flexible visualization
 */
'use client';

import React, { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { config } from '@/lib/config';

// Generic data type for chart data
type ChartData = Record<string, string | number | boolean | null | undefined>;

interface ChartModuleProps {
  data: ChartData[];
  xKey: string;
  yKey: string;
  title: string;
  xLabel?: string;
  yLabel?: string;
  color?: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
}

export function ChartModule({
  data,
  xKey,
  yKey,
  title,
  xLabel,
  yLabel,
  color = '#3b82f6',
  height = 300,
  showGrid = true,
  showLegend = false,
}: ChartModuleProps) {
  // Format data for display - only recalculate when data or xKey changes
  const formattedData = useMemo(() => {
    // If timestamp is not the xKey, no need to format
    if (xKey !== 'timestamp') {
      return data;
    }
    
    return data.map((item) => {
      // Format timestamp for display
      if (typeof item.timestamp === 'string') {
        const date = new Date(item.timestamp);
        return {
          ...item,
          displayTime: date.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          }),
        };
      }
      return item;
    });
  }, [data, xKey]);

  const displayXKey = xKey === 'timestamp' ? 'displayTime' : xKey;

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-lg border border-zinc-200 dark:border-zinc-800 p-4">
      <h3 className="text-lg font-semibold mb-4 text-zinc-900 dark:text-zinc-100">
        {title}
      </h3>
      
      {data.length === 0 ? (
        <div 
          className="flex items-center justify-center text-zinc-500 dark:text-zinc-400"
          style={{ height }}
        >
          Esperando datos...
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={height}>
          <LineChart
            data={formattedData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            {showGrid && (
              <CartesianGrid 
                strokeDasharray="3 3" 
                stroke="#374151"
                opacity={0.3}
              />
            )}
            <XAxis
              dataKey={displayXKey}
              stroke="#6b7280"
              fontSize={12}
              label={xLabel ? { value: xLabel, position: 'bottom', offset: -5 } : undefined}
            />
            <YAxis
              stroke="#6b7280"
              fontSize={12}
              label={yLabel ? { value: yLabel, angle: -90, position: 'insideLeft' } : undefined}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: '1px solid #374151',
                borderRadius: '8px',
                color: '#f3f4f6',
              }}
              labelStyle={{ color: '#9ca3af' }}
            />
            {showLegend && <Legend />}
            <Line
              type="monotone"
              dataKey={yKey}
              stroke={color}
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
              animationDuration={config.chart.animationDuration}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
