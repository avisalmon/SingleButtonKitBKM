#include "SingleButtonKit.h"

Adafruit_SSD1306 screen(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
KitButton button;

static uint8_t screenAddress = 0;

// A contact bounces for a few ms when pressed; ignore changes faster than this.
static constexpr unsigned long DEBOUNCE_MS = 25;

static bool answers(uint8_t address) {
  Wire.beginTransmission(address);
  return Wire.endTransmission() == 0;
}

bool kitBegin() {
  Serial.begin(115200);
  pinMode(KIT_PIN_BUZZER, OUTPUT);
  digitalWrite(KIT_PIN_BUZZER, LOW);
  button.begin();

  Wire.begin(KIT_PIN_SDA, KIT_PIN_SCL);
  Wire.setClock(400000);
  // Most of these screens sit at 0x3C; some boards are strapped to 0x3D.
  if (answers(0x3C)) {
    screenAddress = 0x3C;
  } else if (answers(0x3D)) {
    screenAddress = 0x3D;
  }

  if (screenAddress == 0 || !screen.begin(SSD1306_SWITCHCAPVCC, screenAddress)) {
    screenAddress = 0;
    Serial.println("KIT: screen not found. Check: SDA->21, SCL->22, VCC->3V3, GND->GND.");
    beep(400, 150);
    delay(250);
    beep(400, 150);
    return false;
  }
  screen.clearDisplay();
  screen.setTextColor(SSD1306_WHITE);
  screen.setTextSize(1);
  screen.setCursor(0, 0);
  screen.display();
  return true;
}

uint8_t kitScreenAddress() { return screenAddress; }

void KitButton::begin() {
  pinMode(KIT_PIN_BUTTON, INPUT_PULLUP);
  raw_ = down_ = digitalRead(KIT_PIN_BUTTON) == LOW;
  changedAt_ = millis();
}

void KitButton::update() {
  bool now = digitalRead(KIT_PIN_BUTTON) == LOW;  // pull-up: pressed connects the pin to GND
  unsigned long t = millis();
  if (now != raw_) {
    raw_ = now;
    changedAt_ = t;
  }
  if (down_ != raw_ && t - changedAt_ >= DEBOUNCE_MS) {
    down_ = raw_;
    if (down_) {
      pressedFlag_ = true;
      downSince_ = t;
      count_++;
    } else {
      releasedFlag_ = true;
    }
  }
}

bool KitButton::pressed() {
  bool was = pressedFlag_;
  pressedFlag_ = false;
  return was;
}

bool KitButton::released() {
  bool was = releasedFlag_;
  releasedFlag_ = false;
  return was;
}

unsigned long KitButton::heldFor() const { return down_ ? millis() - downSince_ : 0; }

void beep(unsigned int frequency, unsigned long ms) {
  if (frequency == 0) {
    noTone(KIT_PIN_BUZZER);
    return;
  }
  tone(KIT_PIN_BUZZER, frequency, ms);
}

void silence() { noTone(KIT_PIN_BUZZER); }

void playTune(const unsigned int notes[], const unsigned int durationsMs[], size_t count) {
  for (size_t i = 0; i < count; i++) {
    if (notes[i] != NOTE_REST) {
      tone(KIT_PIN_BUZZER, notes[i]);
    }
    delay(durationsMs[i]);
    noTone(KIT_PIN_BUZZER);
    delay(15);  // a short gap so repeated notes sound separate
  }
}

void printCentered(const char *text, int y, int size) {
  int width = strlen(text) * 6 * size;  // the built-in font is 6 px wide per character
  int x = (SCREEN_WIDTH - width) / 2;
  screen.setTextSize(size);
  screen.setCursor(x < 0 ? 0 : x, y);
  screen.print(text);
}
