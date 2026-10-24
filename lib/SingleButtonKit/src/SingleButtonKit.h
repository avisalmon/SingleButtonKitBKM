// SingleButtonKit: everything a program needs to talk to the kit, in one include.
//
//   #include <SingleButtonKit.h>
//   void setup() { kitBegin(); screen.println("Hello!"); screen.display(); }
//   void loop()  { button.update(); if (button.pressed()) beep(); }
//
// The pins below are the kit's wiring (docs/kit.md). They are checked against the docs by
// tests/test_pins.py, so change them in all three places or not at all.
#pragma once

#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>

// ---- The kit's wiring ----
constexpr int KIT_PIN_SDA = 21;     // OLED SDA
constexpr int KIT_PIN_SCL = 22;     // OLED SCL
constexpr int KIT_PIN_BUTTON = 4;   // button to GND; pressed reads LOW
constexpr int KIT_PIN_BUZZER = 23;  // buzzer +, other leg to GND
constexpr int SCREEN_WIDTH = 128;
constexpr int SCREEN_HEIGHT = 64;

// The screen. Draw on it, then call screen.display() to show what you drew.
// It is an Adafruit_SSD1306: every Adafruit GFX call works (print, drawLine, fillRect, drawBitmap...).
extern Adafruit_SSD1306 screen;

// Start everything: Serial (115200), the screen, the button and the buzzer.
// Returns false if the screen did not answer (it prints why on Serial and buzzes twice).
bool kitBegin();

// The I2C address the screen answered on (0x3C on most kits, 0x3D on some), or 0 if none.
uint8_t kitScreenAddress();

// The one button. Call button.update() once at the top of every loop().
class KitButton {
 public:
  void begin();
  void update();
  bool isDown() const { return down_; }   // held right now
  bool pressed();                          // true once, the moment it goes down
  bool released();                         // true once, the moment it comes up
  unsigned long heldFor() const;           // ms it has been held (0 if up)
  unsigned long presses() const { return count_; }  // presses since start

 private:
  bool down_ = false;
  bool raw_ = false;
  bool pressedFlag_ = false;
  bool releasedFlag_ = false;
  unsigned long changedAt_ = 0;
  unsigned long downSince_ = 0;
  unsigned long count_ = 0;
};
extern KitButton button;

// Sound. beep() does not wait: the program keeps running while the note plays.
void beep(unsigned int frequency = 2000, unsigned long ms = 60);
void silence();
// Plays notes one after another and waits until the tune ends. 0 in notes[] is a rest.
void playTune(const unsigned int notes[], const unsigned int durationsMs[], size_t count);

// Musical notes (Hz) for playTune and beep.
constexpr unsigned int NOTE_C4 = 262, NOTE_D4 = 294, NOTE_E4 = 330, NOTE_F4 = 349, NOTE_G4 = 392,
                       NOTE_A4 = 440, NOTE_B4 = 494, NOTE_C5 = 523, NOTE_D5 = 587, NOTE_E5 = 659,
                       NOTE_F5 = 698, NOTE_G5 = 784, NOTE_A5 = 880, NOTE_REST = 0;

// Write text centred across the screen at row y, in text size 1-4.
void printCentered(const char *text, int y, int size = 1);
