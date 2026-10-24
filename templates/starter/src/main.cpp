// {{NAME}}
// Made with the Single Button kit. Pins and helpers: lib/SingleButtonKit/src/SingleButtonKit.h
#include <SingleButtonKit.h>

void setup() {
  kitBegin();  // starts the screen, the button and the buzzer
  printCentered("{{NAME}}", 28, 1);
  screen.display();
}

void loop() {
  button.update();  // read the button first, every time
  if (button.pressed()) {
    beep();
  }
}
