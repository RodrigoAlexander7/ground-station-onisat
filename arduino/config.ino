#include "HX711.h"

// ==========================================
// --- CONFIGURACIÓN DE PINES ---
// ==========================================
// Balanza
const int DOUT = A1;
const int CLK = A0;
HX711 balanza;
// ¡IMPORTANTE! Ajusta este valor con tu calibración previa
float escala_balanza = 400245.029433; 

// Sensor Infrarrojo (RPM)
const byte pinSensor = 2; // Debe ser pin 2 o 3 en Arduino Uno/Nano

// ==========================================
// --- PARÁMETROS DEL AUTOGIRO ---
// ==========================================
const float numAletas = 4.0; 
// TIEMPO DE REBOTE (Debounce):
// Para 4 aletas, 15ms es mucho tiempo y pierde pulsos a altas RPM.
// Lo bajamos a 3ms. Esto permite medir hasta ~5000 RPM sin perder datos.
const unsigned long tiempoDebounce = 3; 

// ==========================================
// --- VARIABLES GLOBALES ---
// ==========================================
volatile unsigned long contadorPulsos = 0;
volatile unsigned long ultimoTiempoPulso = 0;

unsigned long tiempoAnterior = 0;
float pesoSuavizado = 0;
float fuerzag = 0;

// Variables para promedio de RPM
const int muestrasRPM = 5;
float arrayRPM[muestrasRPM];
int indiceRPM = 0;

void setup() {
  // Velocidad rápida para no perder tiempo imprimiendo
  Serial.begin(115200); 

  // --- CONFIGURACIÓN BALANZA ---
  balanza.begin(DOUT, CLK);
  balanza.set_scale(escala_balanza);
  balanza.tare(20); 

  // --- CONFIGURACIÓN SENSOR IR ---
  pinMode(pinSensor, INPUT);
  
  // Los sensores IR suelen dar señal LOW cuando detectan la aleta (reflejo)
  // Usamos FALLING. Si tu sensor funciona al revés, cambia a RISING.
  attachInterrupt(digitalPinToInterrupt(pinSensor), isrContarPulso, FALLING);
  
  // Limpiar array
  for(int i=0; i<muestrasRPM; i++) arrayRPM[i] = 0;
}

void loop() {
  unsigned long tiempoActual = millis();

  // 1. LECTURA NO BLOQUEANTE DE LA BALANZA
  // Solo leemos si el chip HX711 ya terminó su conversión.
  // Esto evita que el Arduino se quede "congelado" esperando el peso.
  if (balanza.is_ready()) {
    pesoSuavizado = balanza.get_units(1); // Leemos 1 sola vez (dato bruto)
  }

  // 2. CÁLCULO Y MOSTRADO DE DATOS (CADA 1000ms)
  if (tiempoActual - tiempoAnterior >= 1000) {
    
    // --- TOMAR FOTO DE LOS PULSOS ---
    noInterrupts(); // Pausa momentánea de interrupciones para leer variable
    unsigned long pulsos = contadorPulsos;
    contadorPulsos = 0; // Reseteamos cuenta para el siguiente ciclo
    interrupts();   // Reactivamos interrupciones
    
    // Tiempo exacto transcurrido (puede ser 501ms, 502ms, etc.)
    unsigned long deltaTiempo = tiempoActual - tiempoAnterior;

    // --- CÁLCULO MATEMÁTICO RPM ---
    // Fórmula: (Pulsos / Aletas) * (60000ms / tiempo_transcurrido)
    float rpmInstantaneo = (pulsos / numAletas) * (60000.0 / deltaTiempo);

    // --- ENVÍO JSON PARA EL BACKEND ---
    Serial.print("{\"rpm\":");
    Serial.print(rpmInstantaneo, 2);
    Serial.print(",\"lift\":");
    Serial.print(pesoSuavizado, 4);
    Serial.println("}");

    tiempoAnterior = tiempoActual;
  }
}

// ==========================================
// --- RUTINA DE INTERRUPCIÓN (ISR) ---
// ==========================================
// Esta función se ejecuta automáticamente cada vez que pasa una aleta
void isrContarPulso() {
  unsigned long tiempoAhora = millis();
  
  // Filtro Debounce: Si han pasado más de 3ms desde el último pulso, cuenta.
  // Con 4 aletas a 2000 RPM, pasa una aleta cada 7.5ms.
  // 3ms es seguro para evitar falsos positivos sin perder aletas reales.
  if (tiempoAhora - ultimoTiempoPulso > tiempoDebounce) {
    contadorPulsos++;
    ultimoTiempoPulso = tiempoAhora;
  }
}