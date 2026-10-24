// Button beep: a short press plays a note; holding the button makes the tone climb.
// Shows the two ways to read a button: an event (pressed) and a state (isDown, heldFor).
#include <SingleButtonKit.h>

void setup() {
  kitBegin();
  printCentered("Press or hold", 28, 1);
  screen.display();
}

void loop() {
  button.update();  // always first: it reads the pin and notices presses

  if (button.pressed()) {
    beep(NOTE_C5, 80);
  }

  if (button.isDown() && button.heldFor() > 300) {
    unsigned int pitch = 400 + button.heldFor();  // longer hold = higher note
    if (pitch > 3000) pitch = 3000;
    beep(pitch, 30);
    screen.clearDisplay();
    screen.fillRect(0, 54, map(pitch, 400, 3000, 0, 128), 10, SSD1306_WHITE);
    printCentered("Higher!", 20, 2);
    screen.display();
  }

  if (button.released()) {
    silence();
    screen.clearDisplay();
    printCentered("Press or hold", 28, 1);
    screen.display();
  }
}
