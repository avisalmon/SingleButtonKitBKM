// Hello screen: write a name, draw a frame and a smiley.
// The screen is 128 x 64 dots. (0,0) is the top-left corner, (127,63) the bottom-right.
#include <SingleButtonKit.h>

void setup() {
  kitBegin();
  screen.clearDisplay();                         // 1. start from a black screen

  screen.drawRect(0, 0, 128, 64, SSD1306_WHITE);  // 2. a frame around the edge
  printCentered("Hello,", 6, 1);
  printCentered("Maker!", 18, 2);                 // size 2 = twice as big

  screen.drawCircle(64, 50, 10, SSD1306_WHITE);   // 3. a face: circle, two eyes, a smile
  screen.fillCircle(60, 47, 1, SSD1306_WHITE);
  screen.fillCircle(68, 47, 1, SSD1306_WHITE);
  screen.drawLine(59, 53, 64, 56, SSD1306_WHITE);
  screen.drawLine(64, 56, 69, 53, SSD1306_WHITE);

  screen.display();                               // 4. nothing appears until you call display()
}

void loop() {}
