// Jump game: blocks run at you; press the button to jump over them. The game speeds up.
//
// The shape every kit game follows:
//   1. a state (WAITING, PLAYING, OVER) that decides what the loop does,
//   2. read the button, 3. move things, 4. check for hits, 5. draw everything, 6. wait a frame.
// Time comes from millis(), never long delay()s, so the button is always read.
#include <SingleButtonKit.h>

enum State { WAITING, PLAYING, OVER };
State state = WAITING;

const int GROUND = 56;      // y of the ground line
const int PLAYER_X = 16;
const int PLAYER_SIZE = 8;
const int FRAME_MS = 25;    // 40 frames a second

float playerY = GROUND - PLAYER_SIZE;
float playerSpeedY = 0;
float blockX = SCREEN_WIDTH;
int blockHeight = 10;
float blockSpeed = 2.0;
unsigned long score = 0;
unsigned long best = 0;
unsigned long lastFrame = 0;

bool onGround() { return playerY >= GROUND - PLAYER_SIZE; }

void newBlock() {
  blockX = SCREEN_WIDTH + random(0, 40);
  blockHeight = random(6, 16);
}

void startGame() {
  playerY = GROUND - PLAYER_SIZE;
  playerSpeedY = 0;
  blockSpeed = 2.0;
  score = 0;
  newBlock();
  state = PLAYING;
}

void drawWorld() {
  screen.clearDisplay();
  screen.drawLine(0, GROUND, SCREEN_WIDTH - 1, GROUND, SSD1306_WHITE);
  screen.fillRect(PLAYER_X, (int)playerY, PLAYER_SIZE, PLAYER_SIZE, SSD1306_WHITE);
  screen.fillRect((int)blockX, GROUND - blockHeight, 6, blockHeight, SSD1306_WHITE);
  screen.setTextSize(1);
  screen.setCursor(0, 0);
  screen.printf("%lu", score);
  screen.setCursor(80, 0);
  screen.printf("best %lu", best);
}

void setup() {
  kitBegin();
  randomSeed(esp_random());
}

void loop() {
  button.update();
  if (millis() - lastFrame < FRAME_MS) return;
  lastFrame = millis();

  if (state == WAITING || state == OVER) {
    screen.clearDisplay();
    printCentered(state == WAITING ? "JUMP!" : "Ouch!", 10, 3);
    printCentered("press to play", 46, 1);
    screen.display();
    if (button.pressed()) {
      beep(NOTE_C5, 60);
      startGame();
    }
    return;
  }

  // PLAYING
  if (button.pressed() && onGround()) {
    playerSpeedY = -5.5;  // up is negative on the screen
    beep(NOTE_E5, 40);
  }
  playerSpeedY += 0.35;   // gravity
  playerY += playerSpeedY;
  if (onGround()) {
    playerY = GROUND - PLAYER_SIZE;
    playerSpeedY = 0;
  }

  blockX -= blockSpeed;
  if (blockX < -6) {
    newBlock();
    score++;
    blockSpeed += 0.15;   // a little faster every block
    beep(NOTE_G5, 30);
  }

  bool overlapX = blockX < PLAYER_X + PLAYER_SIZE && blockX + 6 > PLAYER_X;
  bool overlapY = playerY + PLAYER_SIZE > GROUND - blockHeight;
  if (overlapX && overlapY) {
    if (score > best) best = score;
    const unsigned int notes[] = {NOTE_G4, NOTE_E4, NOTE_C4};
    const unsigned int times[] = {120, 120, 250};
    playTune(notes, times, 3);
    state = OVER;
    return;
  }

  drawWorld();
  screen.display();
}
