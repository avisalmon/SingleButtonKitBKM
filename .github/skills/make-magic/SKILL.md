---
name: make-magic
description: >
  Turn the learner's idea into a working program on the Single Button kit: interview them briefly, create a project in
  my_projects/, build it in small steps that each run on the kit, and leave them understanding and able to change it.
  Games, animations, music, reaction timers, clocks, WiFi gadgets.
  TRIGGER: "I want to make", "make a game", "make magic", "build me", "new project", "idea", "what can I make",
  "תעשה לי", "אני רוצה לבנות", "משחק", "פרויקט חדש", "רעיון", "מה אפשר לעשות", or kit-guide phase 4 or 5.
---

# Make magic

The learner brings an idea (or picks one); you make it real **with** them, on their kit, in steps they can follow.
How to drive each part of the kit is in the `kit-hardware` skill. Ideas by level: [docs/ideas.md](../../../docs/ideas.md).
A complete one-button game to copy the shape from: [examples/jump_game](../../../examples/jump_game/src/main.cpp).

## 1. Interview (two or three questions, one at a time)

* What should happen? ("A game where a cat jumps over cars"; "a song that plays when I press".)
* What does the button do? (One button: tap, hold, double-tap, count presses. That's the design challenge: enjoy it.)
* How do you win or lose? / When is it finished?

No idea yet? Offer three from docs/ideas.md that fit their age and what they liked so far (PROGRESS.md).
Restate the plan in two lines and get a "yes".

## 2. Create the project

```powershell
.\env\Scripts\python.exe scripts\new_project.py <english_name>
```

Name: lowercase English, digits, `_` (`cat_jump`, `reaction_timer`). Translate a Hebrew idea into a short English name
and tell them ("I called the folder cat_jump").

## 3. Build in small steps; each one runs on the kit

For a game, for example: (1) the player on screen; (2) the button moves it; (3) one obstacle; (4) hitting it ends the
game; (5) score and sound; (6) gets faster. **Upload after every step** (`upload-and-debug`) and ask what they see.
Something they can see or hear within the first two minutes matters more than a complete design.

Code style for learners:
* `#include <SingleButtonKit.h>`, `kitBegin()` in `setup()`, `button.update()` first in `loop()`.
* Short functions with clear English names (`drawCat()`, `checkCrash()`), a one-line comment above each that says
  what it does. Comments can be in Hebrew if the learner reads Hebrew best.
* Numbers the learner will want to tweak go at the top as named constants (`const int JUMP_POWER = 6;`).
* Time with `millis()`, not long `delay()`s, once there is more than one thing happening (kit-hardware: timing).
* Keep everything in `src/main.cpp` until it passes ~200 lines; then split with them, explaining why.

## 4. Hand it over

When it works: show the 2-3 lines that make the magic, and give **one** change to try themselves (speed, sound, size).
Let them do it, upload it for them, cheer. Then offer: a bigger change together, a new project, or `share-my-project`.
Write to `my_projects/PROGRESS.md`: project name, what it does, what they learned, what they want next.

## Using parts the kit does not have

The kit has a screen, one button and a buzzer, plus the ESP32's WiFi and Bluetooth. If an idea needs more (a second
button, a sensor, LEDs), say what part it would need and how it would connect (docs/kit.md lists free pins), and
offer a version that works with the kit as it is. Never ask them to wire something without a clear picture and
"unplug USB first".
