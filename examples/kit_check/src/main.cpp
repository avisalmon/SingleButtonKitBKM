// Kit check: the first program the chat uploads to a newly built kit.
//
// On the screen: "Kit check" and a press counter. Each press beeps.
// On Serial, lines that start with "KITCHECK" so scripts/kit_doctor.py --listen can read the result:
//   KITCHECK i2c=0x3C            every I2C device that answered
//   KITCHECK screen=ok addr=0x3C   or  screen=missing
//   KITCHECK button=up            the button's state at start (should be up)
//   KITCHECK press=1              each press
#include <SingleButtonKit.h>

static void reportI2c() {
  int found = 0;
  for (uint8_t address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    if (Wire.endTransmission() == 0) {
      Serial.printf("KITCHECK i2c=0x%02X\n", address);
      found++;
    }
  }
  if (found == 0) {
    Serial.println("KITCHECK i2c=none");
  }
}

static void drawCount() {
  screen.clearDisplay();
  printCentered("Kit check", 0, 1);
  printCentered("Press the button", 14, 1);
  char count[12];
  snprintf(count, sizeof(count), "%lu", button.presses());
  printCentered(count, 32, 3);
  screen.display();
}

void setup() {
  bool screenOk = kitBegin();
  delay(1500);  // give the computer time to open the port after the reset
  Serial.println();
  Serial.println("KITCHECK start");
  reportI2c();
  if (screenOk) {
    Serial.printf("KITCHECK screen=ok addr=0x%02X\n", kitScreenAddress());
    drawCount();
  } else {
    Serial.println("KITCHECK screen=missing");
  }
  // A button that reads "down" before anyone touches it is usually wired to the wrong pin or to 3V3.
  Serial.printf("KITCHECK button=%s\n", button.isDown() ? "down" : "up");
  const unsigned int notes[] = {NOTE_C5, NOTE_E5, NOTE_G5};
  const unsigned int times[] = {90, 90, 160};
  playTune(notes, times, 3);
  Serial.println("KITCHECK ready");
}

void loop() {
  button.update();
  if (button.pressed()) {
    beep(NOTE_A5, 80);
    Serial.printf("KITCHECK press=%lu\n", button.presses());
    if (kitScreenAddress()) {
      drawCount();
    }
  }
}
