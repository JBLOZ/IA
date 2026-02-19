#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "MAX30105.h"
#include "heartRate.h"

static const int PIN_I2C_SDA = 5;
static const int PIN_I2C_SCL = 6;
static const int PIN_LED_R = 7;
static const int PIN_LED_G = 1;
static const int PIN_LED_B = 0;

static const long FINGER_ENTER_THRESHOLD = 50000;
static const long FINGER_EXIT_THRESHOLD = 42000;

static const unsigned long UI_REFRESH_MS = 200;
static const unsigned long FLASH_MS = 35;
static const unsigned long BEAT_MIN_INTERVAL_MS = 280;
static const unsigned long BEAT_MAX_INTERVAL_MS = 2000;
static const unsigned long FALLBACK_ACTIVATE_MS = 3500;
static const long FALLBACK_HIGH_OFFSET = 4500;
static const long FALLBACK_LOW_OFFSET = 2200;

static const uint8_t RATE_SIZE = 4;

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
MAX30105 particleSensor;

float beatsPerMinute = 0.0f;
int beatAvg = 0;
uint16_t rates[RATE_SIZE];
uint8_t rateSpot = 0;
uint8_t rateCount = 0;

bool fingerPresent = false;
bool flashActive = false;
unsigned long flashUntilMs = 0;
unsigned long lastUiMs = 0;
unsigned long fingerStartMs = 0;
unsigned long lastBeatEdgeMs = 0;
unsigned long lastBeatAnyMs = 0;
unsigned long lastFallbackPeakMs = 0;
bool fallbackAbove = false;
long irBaseline = 0;

void setRgb(bool r, bool g, bool b) {
  digitalWrite(PIN_LED_R, r ? HIGH : LOW);
  digitalWrite(PIN_LED_G, g ? HIGH : LOW);
  digitalWrite(PIN_LED_B, b ? HIGH : LOW);
}

void setBaseColorFromBpm(int bpm) {
  if (bpm < 70) {
    setRgb(false, true, false);
  } else if (bpm < 110) {
    setRgb(true, true, false);
  } else {
    setRgb(true, false, false);
  }
}

void flashWhite() {
  flashActive = true;
  flashUntilMs = millis() + FLASH_MS;
  setRgb(true, true, true);
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
  setBaseColorFromBpm((beatAvg > 0) ? beatAvg : (int)(beatsPerMinute + 0.5f));
  flashWhite();
}

void drawUi() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Pulsometro MAX3010x");
  display.drawLine(0, 10, 127, 10, SSD1306_WHITE);

  if (!fingerPresent) {
    display.setTextSize(2);
    display.setCursor(0, 24);
    display.print("Falta dedo");
  } else if (beatAvg <= 0 && beatsPerMinute <= 0.0f) {
    display.setTextSize(2);
    display.setCursor(0, 22);
    display.print("Midiendo...");
  } else {
    display.setTextSize(2);
    display.setCursor(0, 18);
    display.print("BPM:");
    display.setTextSize(3);
    display.setCursor(0, 38);
    display.print((beatAvg > 0) ? beatAvg : (int)(beatsPerMinute + 0.5f));
  }

  display.display();
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
    setRgb(true, false, false);
    delay(120);
    setRgb(false, false, false);
    delay(120);
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_G, OUTPUT);
  pinMode(PIN_LED_B, OUTPUT);
  setRgb(false, false, false);

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  Wire.setClock(400000);

  bool displayReady = display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  if (!displayReady) {
    haltWithError("ERROR OLED", false);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
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

  resetMeasurementState();
  fingerPresent = false;
  fingerStartMs = 0;
  lastUiMs = millis();
  drawUi();
}

void loop() {
  if (particleSensor.safeCheck(50)) {
    long irValue = particleSensor.getIR();
    unsigned long nowMs = millis();

    if (!fingerPresent && irValue >= FINGER_ENTER_THRESHOLD) {
      fingerPresent = true;
      fingerStartMs = nowMs;
      resetMeasurementState();
      irBaseline = irValue;
      setRgb(false, false, true);
    } else if (fingerPresent && irValue <= FINGER_EXIT_THRESHOLD) {
      fingerPresent = false;
      fingerStartMs = 0;
      resetMeasurementState();
      setRgb(false, false, false);
    }

    if (fingerPresent) {
      if (irBaseline == 0) {
        irBaseline = irValue;
      } else {
        irBaseline = (irBaseline * 15 + irValue) / 16;
      }

      bool beatCaptured = false;

      if (checkForBeat(irValue)) {
        if (lastBeatEdgeMs != 0) {
          unsigned long dtMs = nowMs - lastBeatEdgeMs;
          if (isValidBeatInterval(dtMs)) {
            float bpm = 60000.0f / (float)dtMs;
            registerBeat(bpm, nowMs);
            beatCaptured = true;
          }
        }
        lastBeatEdgeMs = nowMs;
      }

      unsigned long referenceMs = (lastBeatAnyMs == 0) ? fingerStartMs : lastBeatAnyMs;
      if (!beatCaptured && referenceMs != 0 && (nowMs - referenceMs) >= FALLBACK_ACTIVATE_MS) {
        long highThreshold = irBaseline + FALLBACK_HIGH_OFFSET;
        long lowThreshold = irBaseline + FALLBACK_LOW_OFFSET;

        if (!fallbackAbove && irValue > highThreshold) {
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

        if (fallbackAbove && irValue < lowThreshold) {
          fallbackAbove = false;
        }
      }

      if (beatAvg <= 0 && beatsPerMinute <= 0.0f && !flashActive) {
        setRgb(false, false, true);
      }
    }
  }

  if (flashActive && millis() >= flashUntilMs) {
    flashActive = false;
    if (!fingerPresent) {
      setRgb(false, false, false);
    } else if (beatAvg > 0 || beatsPerMinute > 0.0f) {
      setBaseColorFromBpm((beatAvg > 0) ? beatAvg : (int)(beatsPerMinute + 0.5f));
    } else {
      setRgb(false, false, true);
    }
  }

  if (millis() - lastUiMs >= UI_REFRESH_MS) {
    lastUiMs = millis();
    drawUi();
  }
}
