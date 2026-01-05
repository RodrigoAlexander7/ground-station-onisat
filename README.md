# Wind Tunnel Data Acquisition System

Sistema de adquisición, logueo y visualización de datos en tiempo real para túnel de viento.

## 🏗️ Arquitectura

### Backend (FastAPI)
Implementa el patrón **Puertos y Adaptadores** (Hexagonal Architecture):

```
backend/
├── app/
│   ├── core/           # Domain layer
│   │   ├── models.py   # Pydantic models (SystemReading, etc.)
│   │   └── config.py   # Application settings
│   ├── ports/          # Abstract interfaces
│   │   ├── sensor_port.py  # Sensor interface
│   │   └── data_port.py    # Persistence interface
│   ├── adapters/       # Implementations
│   │   ├── arduino_adapter.py     # Real Arduino via Serial
│   │   ├── mock_arduino_adapter.py # Mock for testing
│   │   └── json_data_adapter.py   # JSON file persistence
│   ├── services/       # Business logic
│   │   ├── measurement_manager.py  # Main orchestrator
│   │   └── connection_manager.py   # WebSocket management
│   ├── api/            # HTTP/WS endpoints
│   │   ├── websocket.py    # WebSocket endpoint
│   │   └── routes.py       # REST API routes
│   └── main.py         # FastAPI application
```

### Frontend (Next.js)
```
frontend/
├── app/
│   └── page.tsx        # Main dashboard
├── components/
│   ├── ChartModule.tsx     # Reusable chart component
│   ├── WindSpeedControl.tsx # Wind speed input
│   ├── StatusPanel.tsx     # System status
│   ├── CurrentReadings.tsx # Real-time readings
│   └── CustomChart.tsx     # Configurable X/Y chart
├── lib/
│   ├── store.ts        # Zustand state management
│   ├── useWebSocket.ts # WebSocket hook
│   ├── types.ts        # TypeScript types
│   └── config.ts       # Configuration
```

## 🚀 Quick Start

### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar (modo mock por defecto)
python -m uvicorn app.main:app --reload
```

El backend estará en `http://localhost:8000`

### 2. Frontend

```bash
cd frontend

# Instalar dependencias
pnpm install

# Ejecutar
pnpm dev
```

El frontend estará en `http://localhost:3000`

## ⚙️ Configuración

### Backend (.env)
```env
# Usar mock o Arduino real
USE_MOCK_ARDUINO=true

# Puerto serial para Arduino
SERIAL_PORT=/dev/ttyUSB0
SERIAL_BAUDRATE=9600

# Intervalo de lectura (segundos)
READING_INTERVAL=0.1
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 📡 Flujo de Datos

```
┌─────────────┐      WebSocket       ┌─────────────┐
│   Frontend  │◄────────────────────►│   Backend   │
│  (Next.js)  │  wind_speed input    │  (FastAPI)  │
└─────────────┘                      └──────┬──────┘
                                            │
                                   ┌────────▼────────┐
                                   │ MeasurementMgr  │
                                   └────────┬────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
                │ ArduinoAdapter│  │ WindInput     │  │ JsonDataAdapter│
                │ (Serial/Mock) │  │ (from WS)     │  │ (persistence)  │
                └───────────────┘  └───────────────┘  └───────────────┘
```

1. **Frontend** envía velocidad de viento vía WebSocket
2. **Backend** almacena el valor en memoria
3. **Loop de lectura** obtiene RPM/Sustentación del Arduino
4. **Fusión**: `{timestamp, wind_speed, rpm, lift_force}`
5. **Persistencia**: Guardado en JSON (si recording activo)
6. **Broadcast**: Envío a todos los clientes WebSocket

## 📊 API Endpoints

### REST API
- `GET /api/status` - Estado del sistema
- `GET /api/readings?limit=100` - Últimas lecturas
- `POST /api/wind-speed` - Establecer velocidad de viento
- `POST /api/recording/start` - Iniciar grabación
- `POST /api/recording/stop` - Detener grabación
- `DELETE /api/readings` - Limpiar lecturas

### WebSocket (`/ws`)
**Mensajes que recibe:**
```json
{"type": "wind_speed", "value": 10.5}
{"type": "command", "action": "start_recording"}
{"type": "command", "action": "stop_recording"}
{"type": "command", "action": "clear"}
```

**Mensajes que envía:**
```json
{"timestamp": "2026-01-05T...", "wind_speed": 10.5, "rpm": 1500, "lift_force": 2.5}
{"type": "status", "data": {...}}
```

## 🔧 Arduino Setup

El Arduino debe enviar datos JSON por Serial:
```json
{"rpm": 1500.0, "lift": 2.5}
```

Ejemplo de código Arduino:
```cpp
void loop() {
  float rpm = readRPM();
  float lift = readLiftForce();
  
  Serial.print("{\"rpm\":");
  Serial.print(rpm);
  Serial.print(",\"lift\":");
  Serial.print(lift);
  Serial.println("}");
  
  delay(100);
}
```

## 📁 Estructura de Datos JSON

Los datos se guardan en `backend/data/readings.json`:
```json
[
  {
    "timestamp": "2026-01-05T10:30:00.123456",
    "wind_speed": 10.5,
    "rpm": 1523.45,
    "lift_force": 2.34
  },
  ...
]
```

## 🛠️ Desarrollo

### Modo Mock (sin Arduino)
Por defecto, el backend usa un adaptador mock que genera datos simulados.
Para usar Arduino real:
```env
USE_MOCK_ARDUINO=false
```

### Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
pnpm test
```

## 📝 License

MIT License - ONISAT Ground Station Project
