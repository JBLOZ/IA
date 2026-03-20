#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <PubSubClient.h>
#include "arduino_secrets.h"

// --- PINES ---
#define SDA_PIN 5
#define SCL_PIN 6
#define LED_R 7 

// --- CONFIGURACIÓN OLED ---
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// --- CONFIGURACIÓN SENSOR Y FILTRO ---
MAX30105 particleSensor;
const byte RATE_SIZE = 4; 
long rates[RATE_SIZE]; 
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute;
int beatAvg = 0;

// --- VARIABLES PARTE A (BATERÍA) ---
unsigned long lastSendTime = 0;
int lastSentValue = 0;
const int threshold = 5;
const unsigned long sendInterval = 30000; 
unsigned long lastAlarmTime = 0;

// Variables para el mensaje visual en pantalla
unsigned long tiempoAvisoOLED = 0;
String motivoAviso = "";

// --- MQTT ---
const char* mqtt_server = "192.168.0.106"; 
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi_and_diagnostics() {
  WiFi.begin(SECRET_SSID, SECRET_PASS);
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500); 
    Serial.print("."); 
  }
  
  Serial.println("\n--- Diagnóstico de Red ---");
  Serial.print("IP: "); Serial.println(WiFi.localIP());
  Serial.print("MAC: "); Serial.println(WiFi.macAddress());
  Serial.print("RSSI: "); Serial.print(WiFi.RSSI()); Serial.println(" dBm");

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0,0);
  display.println("WiFi OK!");
  display.print("IP: "); display.println(WiFi.localIP());
  display.print("RSSI: "); display.print(WiFi.RSSI()); display.println("dBm");
  display.display();
  delay(3000); 
}

void callback(char* topic, uint8_t* payload, unsigned int length) {
  if ((char)payload[0] == '1') {
    digitalWrite(LED_R, HIGH); 
  } else {
    digitalWrite(LED_R, LOW);
  }
}

void reconnect() {
  while (!client.connected()) {
    String clientId = "ESP32_MV_" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      client.subscribe("clase/salud/MV/ordenes");
    } else {
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  Wire.begin(SDA_PIN, SCL_PIN);
  
  pinMode(LED_R, OUTPUT);
  digitalWrite(LED_R, LOW);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println("Error OLED");
    for(;;);
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  setup_wifi_and_diagnostics();

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("Error MAX30105");
    display.clearDisplay();
    display.setCursor(0,0);
    display.print("Sensor no detectado");
    display.display();
    for(;;);
  }
  particleSensor.setup(); 
  particleSensor.setPulseAmplitudeRed(0x0A); 

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue) == true && irValue > 50000) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (long)beatsPerMinute;
      rateSpot %= RATE_SIZE;
      beatAvg = 0;
      for (byte x = 0 ; x < RATE_SIZE ; x++) beatAvg += rates[x];
      beatAvg /= RATE_SIZE; 
    }
  }

  unsigned long currentTime = millis();
  
  bool alarmCondition = (beatAvg > 160 && (currentTime - lastAlarmTime > 60000));
  bool timeToSend = (currentTime - lastSendTime > sendInterval);
  bool thresholdMet = (abs(beatAvg - lastSentValue) >= threshold);

  if (irValue > 50000) { 
    
    // Si se cumple alguna regla, disparamos el envío
    if (timeToSend || thresholdMet || alarmCondition) {
      char msg[10];
      dtostrf(beatAvg, 1, 0, msg);
      
      client.publish("clase/salud/MV/datos", msg);
      
      lastSentValue = beatAvg;
      lastSendTime = currentTime;
      if (alarmCondition) lastAlarmTime = currentTime;

      // Guardamos el motivo y el tiempo para que se muestre en pantalla
      tiempoAvisoOLED = currentTime;
      if (alarmCondition) motivoAviso = "Regla C (Alarma)";
      else if (thresholdMet) motivoAviso = "Regla B (Umbral)";
      else motivoAviso = "Regla A (Tiempo)";

      // Aviso claro por el Monitor Serie
      Serial.println("\n==================================");
      Serial.print(">> ENVIANDO PULSACIONES: ");
      Serial.print(beatAvg);
      Serial.println(" BPM");
      Serial.print(">> MOTIVO: ");
      Serial.println(motivoAviso);
      Serial.println("==================================\n");
    }

    display.clearDisplay();
    
    // Mostrar el pulso actual
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print("BPM: "); display.print(beatAvg);

    // Si hace menos de 2000 milisegundos (2 segundos) que enviamos el dato, mostrar el mensaje
    if (currentTime - tiempoAvisoOLED < 2000) {
      display.setTextSize(1);
      display.setCursor(0, 20);
      display.print("ENVIADO: ");
      display.print(motivoAviso);
    }

    display.display();

  } else {
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 10);
    display.print("Pon el dedo");
    display.display();
    beatAvg = 0; 
  }
}