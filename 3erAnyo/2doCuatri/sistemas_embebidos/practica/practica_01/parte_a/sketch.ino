// Práctica 1 - Sistemas Embebidos - PARTE A
// Simulación con Wokwi: LED Blink, OLED y Potenciómetro

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Definición de pines
#define LED_BLINK 2      // LED para secuencia de parpadeos
#define POT_PIN 0        // Potenciómetro (simula sensor MAX30105)
#define SDA_PIN 8        // I2C SDA
#define SCL_PIN 9        // I2C SCL

// Configuración OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int bpm = 0;
int lectura = 0;

void setup() {
  Serial.begin(115200);
  
  // Configurar pines
  pinMode(LED_BLINK, OUTPUT);
  pinMode(POT_PIN, INPUT);
  
  // Inicializar I2C
  Wire.begin(SDA_PIN, SCL_PIN);
  
  // Inicializar OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Error: No se detectó la pantalla SSD1306"));
    for(;;);
  }
  
  // Mostrar mensaje inicial en OLED
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 20);
  display.println(F("Iniciando"));
  display.println(F("..."));
  display.display();
  
  Serial.println("Sistema iniciado - Parte A");
  Serial.println("Esperando 2 segundos...");
  
  delay(2000);
  
  // PARTE A.2: Secuencia de 5 parpadeos rápidos (100ms) + pausa de 1 segundo
  Serial.println("Ejecutando secuencia de blink: 5 parpadeos rápidos");
  for(int i = 0; i < 5; i++) {
    digitalWrite(LED_BLINK, HIGH);
    delay(100);
    digitalWrite(LED_BLINK, LOW);
    delay(100);
    Serial.print("Parpadeo ");
    Serial.println(i + 1);
  }
  Serial.println("Pausa de 1 segundo...");
  delay(1000);
  Serial.println("Secuencia de blink completada");
  Serial.println("Iniciando lectura de sensor simulado...");
}

void loop() {
  // PARTE A.4: Leer potenciómetro y simular sensor
  lectura = analogRead(POT_PIN);
  
  // Mapear lectura a BPM (40-180) según especificaciones
  bpm = map(lectura, 0, 4095, 40, 180);
  
  // PARTE A.3: Mostrar en Monitor Serial
  Serial.print("Lectura: ");
  Serial.print(lectura);
  Serial.print(" -> BPM: ");
  Serial.println(bpm);
  
  // PARTE A.3: Actualizar pantalla OLED con BPM
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 10);
  display.println(F("BPM:"));
  display.setTextSize(3);
  display.setCursor(20, 35);
  display.println(bpm);
  display.display();
  
  // Parpadeo simple del LED para indicar actividad
  digitalWrite(LED_BLINK, HIGH);
  delay(50);
  digitalWrite(LED_BLINK, LOW);
  
  delay(450); // Total 500ms por ciclo
}