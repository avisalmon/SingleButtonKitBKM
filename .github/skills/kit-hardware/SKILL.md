---
name: kit-hardware
description: >
  How to drive every part of the Single Button kit in Arduino C++ with the SingleButtonKit library: drawing and
  text on the 128x64 OLED (including Hebrew text), animation, pictures, the button (tap, hold, double-tap), sound and
  tunes on the buzzer, timing with millis, random numbers, saving a high score, WiFi and internet time.
  TRIGGER: "draw", "screen", "text", "Hebrew on the screen", "animation", "picture", "sprite", "button", "long press",
  "double click", "sound", "music", "melody", "timer", "random", "save score", "wifi", "clock", "internet",
  "ציור", "מסך", "עברית", "אנימציה", "כפתור", "צליל", "מנגינה", "שעון", "אינטרנט".
---

# Kit hardware recipes

Pins and wiring: [docs/kit.md](../../../docs/kit.md). The library: [SingleButtonKit.h](../../../lib/SingleButtonKit/src/SingleButtonKit.h).
Every recipe below assumes `#include <SingleButtonKit.h>`, `kitBegin()` in `setup()` and `button.update()` first in `loop()`.

## Screen

`screen` is an `Adafruit_SSD1306` (Adafruit GFX). 128 x 64 dots, (0,0) top-left, colours `SSD1306_WHITE` / `SSD1306_BLACK`.
**Draw, then `screen.display()`**: nothing shows until then. For animation: `clearDisplay()`, draw everything, `display()`, every frame.

```cpp
screen.clearDisplay();
screen.drawPixel(x, y, SSD1306_WHITE);
screen.drawLine(x0, y0, x1, y1, SSD1306_WHITE);
screen.drawRect(x, y, w, h, SSD1306_WHITE);   screen.fillRect(...);
screen.drawCircle(x, y, r, SSD1306_WHITE);    screen.fillCircle(...);
screen.drawRoundRect(x, y, w, h, r, SSD1306_WHITE);
screen.drawTriangle(x0, y0, x1, y1, x2, y2, SSD1306_WHITE);
screen.setTextSize(2); screen.setCursor(0, 0); screen.print("Hi"); screen.printf("%d", score);
printCentered("GAME OVER", 24, 2);            // from the kit library
screen.invertDisplay(true);                   // flash effect
screen.display();
```

Text size 1 = 6x8 dots per letter (21 letters x 8 lines); size 2 = 12x16; size 3 = 18x24.
The built-in font has **English letters only**. A full frame redraw takes ~25 ms at 400 kHz: ~30-40 frames a second.

### Pictures (sprites)

A 1-bit picture as bytes, drawn with `drawBitmap`. Each row is padded to whole bytes; `1` = lit.

```cpp
const unsigned char PROGMEM heart[] = {   // 8 x 7
  0b01100110, 0b11111111, 0b11111111, 0b11111111, 0b01111110, 0b00111100, 0b00011000 };
screen.drawBitmap(x, y, heart, 8, 7, SSD1306_WHITE);
```

Design small sprites with the learner as rows of 0/1 (they can draw on squared paper). For animation, keep 2-3 frames and
switch every ~150 ms.

### Hebrew text (tested to build; uses one extra library)

Add to the project's `platformio.ini` under `[env:kit]`:

```ini
lib_deps =
    ${kit.lib_deps}
    olikraus/U8g2_for_Adafruit_GFX@1.8.0
```

```cpp
#include <U8g2_for_Adafruit_GFX.h>
U8G2_FOR_ADAFRUIT_GFX hebrew;

// Hebrew reads right-to-left but fonts draw left-to-right: reverse the letters first.
// (Numbers inside get reversed too, so print numbers separately.)
String rtl(const char *text) {
  String out, letter;
  for (const char *p = text; *p; p++) {
    letter += *p;
    if ((p[1] & 0xC0) != 0x80) {  // the next byte starts a new UTF-8 letter
      out = letter + out;
      letter = "";
    }
  }
  return out;
}

void printHebrewCentered(const char *text, int baselineY) {
  String shown = rtl(text);
  int x = (SCREEN_WIDTH - hebrew.getUTF8Width(shown.c_str())) / 2;
  hebrew.setCursor(x < 0 ? 0 : x, baselineY);   // y is the text's baseline, not its top
  hebrew.print(shown.c_str());
}

// in setup(), after kitBegin():
hebrew.begin(screen);
hebrew.setFont(u8g2_font_unifont_t_hebrew);       // 16 px high: about 3 lines fit
hebrew.setForegroundColor(SSD1306_WHITE);
printHebrewCentered("שלום עולם", 24);
screen.display();
```

## Button

```cpp
if (button.pressed())  { ... }            // once per press (debounced)
if (button.released()) { ... }            // once, when let go
if (button.isDown())   { ... }            // every loop while held
if (button.isDown() && button.heldFor() > 800) { ... }   // long press
button.presses();                           // count since start
```

Tap vs long press, decided on release:
```cpp
static unsigned long heldMs = 0;
if (button.isDown()) heldMs = button.heldFor();
if (button.released()) { if (heldMs > 600) longPress(); else tap(); }
```

Double-tap: remember the time of the last tap; a second tap within ~300 ms is a double. Decide a single tap only after
300 ms pass with no second one. **One-button design ideas**: tap = jump, hold = charge power, release = fire; or
tap = next option, hold = choose (menus); or Morse-style (short/long) input.

## Sound

```cpp
beep();                         // short 2 kHz beep, does not wait
beep(NOTE_A4, 200);             // a note for 200 ms, does not wait
silence();
const unsigned int notes[] = {NOTE_C5, NOTE_E5, NOTE_G5, NOTE_REST, NOTE_C5};
const unsigned int times[] = {150, 150, 150, 100, 400};
playTune(notes, times, 5);      // waits until the tune ends: use between rounds, not during play
```

Sound effects that don't stop the game: call `beep(freq, ms)` with a short `ms`; a falling "laser": over a few frames
`beep(2000 - frame * 150, 30)`. During play, never a long `playTune`: it freezes the game.
The kit's buzzer is driven with a tone (PWM) on pin 23. If a buzzer only clicks, it is an "active" buzzer: it can only beep.

## Timing: do several things at once

`delay()` freezes everything, including the button. Use `millis()` (ms since start):

```cpp
unsigned long lastMove = 0;
void loop() {
  button.update();
  if (millis() - lastMove >= 50) {   // every 50 ms
    lastMove = millis();
    moveEnemies();
  }
  if (button.pressed()) jump();       // still instant
}
```

Several timers = several `lastX` variables. A game frame: `if (millis() - lastFrame < 25) return;` at the top of `loop()`
(see examples/jump_game).

## Random

`randomSeed(esp_random());` once in `setup()` (the ESP32 has a true random generator), then `random(10, 50)` = 10..49.

## Save something across power-off (high score)

```cpp
#include <Preferences.h>
Preferences store;
store.begin("game", false);
int best = store.getInt("best", 0);
store.putInt("best", score);      // only when it changes: flash wears out after ~100,000 writes
```

## WiFi and internet time

Passwords never go in `main.cpp`. Create `include/secrets.h` in the project (it is inside my_projects/, so never
committed), and make sure the learner knows not to share it:

```cpp
// include/secrets.h
#define WIFI_NAME "..."
#define WIFI_PASSWORD "..."
```

```cpp
#include <WiFi.h>
#include <time.h>
#include "secrets.h"

WiFi.begin(WIFI_NAME, WIFI_PASSWORD);
unsigned long start = millis();
while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) delay(200);
if (WiFi.status() == WL_CONNECTED) {
  configTzTime("IST-2IDT,M3.4.4/26,M10.5.0", "pool.ntp.org");   // Israel time, summer time included
  struct tm now;
  if (getLocalTime(&now)) screen.printf("%02d:%02d", now.tm_hour, now.tm_min);
}
```

The ESP32 joins **2.4 GHz** networks only. A phone hotspot works well for a class. Note: WiFi settings are kept in the
kit's flash after this, so a flash dump of a kit that used WiFi contains the password (gotchas #6).

## Free pins for extra parts

Free and safe on the kit: 13, 14, 16, 17, 18, 19, 25, 26, 27, 32, 33. Inputs only: 34, 35, 36 (VP), 39 (VN).
Avoid 0, 2, 5, 12, 15 (they decide how the board starts), 1 and 3 (USB serial), 6-11 (flash).
A second button: like the first (pin -> button -> GND, `INPUT_PULLUP`). An LED: pin -> 220 Ω resistor -> LED long leg,
short leg -> GND.
