/*
  Practica 2 - Comunicaciones y procesado
  ESP32-C3 + MAX3010x + OLED + MQTT

  Lee el pulsometro real, muestra el estado en pantalla OLED y publica
  el BPM medio en MQTT para el dashboard.
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "MAX30105.h"
#include "heartRate.h"

#ifndef LED_BUILTIN
#define LED_BUILTIN 8
#endif

static const char *ssid = "TP-Link_7BC5";
static const char *password = "81912834";
static const char *mqttServer = "192.168.0.106";
static const uint16_t mqttPort = 1883;

static const char *topicData = "outTopic";
static const char *topicStatus = "practica2/esp32/estado";
static const char *topicControl = "inTopic";

static const int PIN_I2C_SDA = 5;
static const int PIN_I2C_SCL = 6;

static const long FINGER_ENTER_THRESHOLD = 50000;
static const long FINGER_EXIT_THRESHOLD = 42000;
static const unsigned long UI_REFRESH_MS = 200;
static const unsigned long MQTT_PUBLISH_MS = 2000;
static const unsigned long BEAT_MIN_INTERVAL_MS = 280;
static const unsigned long BEAT_MAX_INTERVAL_MS = 2000;
static const unsigned long FALLBACK_ACTIVATE_MS = 3500;
static const long FALLBACK_HIGH_OFFSET = 4500;
static const long FALLBACK_LOW_OFFSET = 2200;

static const uint8_t RATE_SIZE = 4;
static const int SCREEN_WIDTH = 128;
static const int SCREEN_HEIGHT = 64;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
MAX30105 particleSensor;

float beatsPerMinute = 0.0f;
int beatAvg = 0;
uint16_t rates[RATE_SIZE];
uint8_t rateSpot = 0;
uint8_t rateCount = 0;

bool fingerPresent = false;
unsigned long bootCount = 0;
unsigned long lastUiMs = 0;
unsigned long lastPublishMs = 0;
unsigned long fingerStartMs = 0;
unsigned long lastBeatEdgeMs = 0;
unsigned long lastBeatAnyMs = 0;
unsigned long lastFallbackPeakMs = 0;
bool fallbackAbove = false;
long irBaseline = 0;

char payload[192];

void connectWiFi();
void ensureMqttConnection();
void mqttCallback(char *topic, byte *incomingPayload, unsigned int length);
void publishStatus(const char *message);
void drawUi(long irValue);
void resetMeasurementState();
bool isValidBeatInterval(unsigned long dtMs);
void registerBeat(float bpm, unsigned long nowMs);
void haltWithError(const char *message, bool canDraw);

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  Wire.setClock(400000);

  bool displayReady = display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  if (!displayReady) {
    haltWithError("ERROR OLED", false);
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Iniciando...");
  display.display();

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    haltWithError("ERROR MAX3010x", true);
  }

  byte ledBrightness = 0x1F;
  byte sampleAverage = 4;
  byte ledMode = 2;
  int sampleRate = 100;
  int pulseWidth = 411;
  int adcRange = 4096;
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
  particleSensor.setPulseAmplitudeRed(0x1F);
  particleSensor.setPulseAmplitudeIR(0x1F);
  particleSensor.setPulseAmplitudeGreen(0x00);

  connectWiFi();
  mqttClient.setServer(mqttServer, mqttPort);
  mqttClient.setCallback(mqttCallback);

  resetMeasurementState();
  drawUi(0);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  ensureMqttConnection();
  mqttClient.loop();

  long currentIrValue = 0;
  unsigned long nowMs = millis();

  if (particleSensor.safeCheck(50)) {
    currentIrValue = particleSensor.getIR();

    if (!fingerPresent && currentIrValue >= FINGER_ENTER_THRESHOLD) {
      fingerPresent = true;
      fingerStartMs = nowMs;
      resetMeasurementState();
      irBaseline = currentIrValue;
    } else if (fingerPresent && currentIrValue <= FINGER_EXIT_THRESHOLD) {
      fingerPresent = false;
      fingerStartMs = 0;
      resetMeasurementState();
    }

    if (fingerPresent) {
      if (irBaseline == 0) {
        irBaseline = currentIrValue;
      } else {
        irBaseline = (irBaseline * 15 + currentIrValue) / 16;
      }

      bool beatCaptured = false;

      if (checkForBeat(currentIrValue)) {
        digitalWrite(LED_BUILTIN, HIGH);
        if (lastBeatEdgeMs != 0) {
          unsigned long dtMs = nowMs - lastBeatEdgeMs;
          if (isValidBeatInterval(dtMs)) {
            float bpm = 60000.0f / (float)dtMs;
            registerBeat(bpm, nowMs);
            beatCaptured = true;
          }
        }
        lastBeatEdgeMs = nowMs;
      } else {
        digitalWrite(LED_BUILTIN, LOW);
      }

      unsigned long referenceMs = (lastBeatAnyMs == 0) ? fingerStartMs : lastBeatAnyMs;
      if (!beatCaptured && referenceMs != 0 && (nowMs - referenceMs) >= FALLBACK_ACTIVATE_MS) {
        long highThreshold = irBaseline + FALLBACK_HIGH_OFFSET;
        long lowThreshold = irBaseline + FALLBACK_LOW_OFFSET;

        if (!fallbackAbove && currentIrValue > highThreshold) {
          fallbackAbove = true;
          if (lastFallbackPeakMs != 0) {
            unsigned long dtMs = nowMs - lastFallbackPeakMs;
            if (isValidBeatInterval(dtMs)) {
              float bpm = 60000.0f / (float)dtMs;
              registerBeat(bpm, nowMs);
            }
          }
          lastFallbackPeakMs = nowMs;
        }

        if (fallbackAbove && currentIrValue < lowThreshold) {
          fallbackAbove = false;
        }
      }
    } else {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }

  if (nowMs - lastUiMs >= UI_REFRESH_MS) {
    lastUiMs = nowMs;
    drawUi(currentIrValue);
  }

  if (nowMs - lastPublishMs >= MQTT_PUBLISH_MS) {
    lastPublishMs = nowMs;

    if (fingerPresent && beatAvg > 0) {
      snprintf(payload, sizeof(payload), "%d", beatAvg);
      Serial.print("MQTT outTopic -> ");
      Serial.println(payload);
      mqttClient.publish(topicData, payload);
    } else {
      publishStatus(fingerPresent ? "midiendo" : "sin_dedo");
    }
  }
}

void connectWiFi() {
  Serial.print("Conectando a WiFi ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado");
  Serial.print("IP local: ");
  Serial.println(WiFi.localIP());
}

void ensureMqttConnection() {
  while (!mqttClient.connected()) {
    Serial.print("Conectando al broker MQTT...");

    String clientId = "esp32c3-practica2-";
    clientId += String((uint32_t)ESP.getEfuseMac(), HEX);
    clientId += "-";
    clientId += String(bootCount++);

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println(" conectado");
      mqttClient.subscribe(topicControl);
      publishStatus("mqtt_connected");
    } else {
      Serial.print(" fallo rc=");
      Serial.print(mqttClient.state());
      Serial.println(" reintentando en 3 segundos");
      delay(3000);
    }
  }
}

void mqttCallback(char *topic, byte *incomingPayload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)incomingPayload[i];
  }

  Serial.print("MQTT [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(msg);

  if (String(topic) == topicControl) {
    digitalWrite(LED_BUILTIN, (msg == "1") ? HIGH : LOW);
  }
}

void publishStatus(const char *message) {
  snprintf(
    payload,
    sizeof(payload),
    "{\"device\":\"esp32-c3\",\"status\":\"%s\",\"ip\":\"%s\",\"bpm\":%d}",
    message,
    WiFi.localIP().toString().c_str(),
    beatAvg
  );
  mqttClient.publish(topicStatus, payload, true);
}

void drawUi(long irValue) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Practica 2 MAX3010x");
  display.drawLine(0, 10, 127, 10, SSD1306_WHITE);

  if (!fingerPresent) {
    display.setTextSize(2);
    display.setCursor(0, 20);
    display.print("Falta dedo");
  } else if (beatAvg <= 0 && beatsPerMinute <= 0.0f) {
    display.setTextSize(2);
    display.setCursor(0, 20);
    display.print("Midiendo...");
  } else {
    display.setTextSize(2);
    display.setCursor(0, 16);
    display.print("BPM:");
    display.setTextSize(3);
    display.setCursor(0, 36);
    display.print((beatAvg > 0) ? beatAvg : (int)(beatsPerMinute + 0.5f));
  }

  display.setTextSize(1);
  display.setCursor(0, 56);
  display.print("IR:");
  display.print(irValue);
  display.display();
}

void resetMeasurementState() {
  beatsPerMinute = 0.0f;
  beatAvg = 0;
  rateSpot = 0;
  rateCount = 0;
  for (uint8_t i = 0; i < RATE_SIZE; i++) {
    rates[i] = 0;
  }
  lastBeatEdgeMs = 0;
  lastBeatAnyMs = 0;
  lastFallbackPeakMs = 0;
  fallbackAbove = false;
  irBaseline = 0;
}

bool isValidBeatInterval(unsigned long dtMs) {
  return dtMs >= BEAT_MIN_INTERVAL_MS && dtMs <= BEAT_MAX_INTERVAL_MS;
}

void registerBeat(float bpm, unsigned long nowMs) {
  if (bpm < 30.0f || bpm > 220.0f) {
    return;
  }

  beatsPerMinute = bpm;
  rates[rateSpot] = (uint16_t)(bpm + 0.5f);
  rateSpot = (rateSpot + 1) % RATE_SIZE;
  if (rateCount < RATE_SIZE) {
    rateCount++;
  }

  uint32_t sum = 0;
  for (uint8_t i = 0; i < rateCount; i++) {
    sum += rates[i];
  }
  beatAvg = (rateCount == 0) ? 0 : (int)(sum / rateCount);
  lastBeatAnyMs = nowMs;
}

void haltWithError(const char *message, bool canDraw) {
  Serial.println(message);

  if (canDraw) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print(message);
    display.display();
  }

  while (true) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(120);
    digitalWrite(LED_BUILTIN, LOW);
    delay(120);
  }
}
