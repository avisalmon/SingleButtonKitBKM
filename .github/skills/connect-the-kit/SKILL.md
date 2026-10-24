---
name: connect-the-kit
description: >
  Find the Single Button kit on USB, prove the ESP32 answers, and prove the screen, button and buzzer are wired
  right using the kit_check program and kit_doctor. Diagnoses by symptom: no COM port, screen dark, no sound,
  button dead or always pressed, Flappy not working after assembly.
  TRIGGER: "connect the kit", "is my kit working", "check my kit", "kit not found", "no COM port", "screen is black",
  "no sound", "button doesn't work", "Flappy doesn't work", "הערכה לא עובדת", "המסך שחור", "אין צליל", "הכפתור לא עובד",
  or kit-guide phase 1 or 3.
---

# Connect the kit

The wiring is in [docs/kit.md](../../../docs/kit.md) (pins, a table and a picture). Known traps are in
[docs/gotchas.md](../../../docs/gotchas.md). Read both before diagnosing.

## A. Is it on USB?

`.\env\Scripts\python.exe scripts\kit_doctor.py`. Act on its FAIL lines; it says what to do. Most common: a
charge-only cable, a missing driver (`setup-my-computer` step 3), or another program holding the port (Thonny,
Arduino IDE, a serial monitor).

## B. Does the ESP32 answer?

`.\env\Scripts\python.exe scripts\kit_doctor.py --chip` -> chip type, flash size, MAC.
If it does not answer: ask the learner to **hold the BOOT button** (the small button to the right of the USB socket),
run it again, and let go when "Connecting..." appears (gotchas #3).

## C. Do the parts work? (replaces Flappy: tell the learner first, CLAUDE.md rule 5)

```powershell
$env:PYTHONIOENCODING="utf-8"; .\env\Scripts\pio.exe run -d examples\kit_check -t upload
```

Then say "Press the button a few times now" and run `.\env\Scripts\python.exe scripts\kit_doctor.py --listen 20`.
It reads the KITCHECK lines and reports screen, button and presses. Ask the learner: did you hear three rising
notes, and a beep with each press? Does the screen count your presses?

## Diagnose by symptom (ask what they see, then check one wire at a time)

Always: **unplug USB before touching wires**, then replug.

| Symptom | Most likely | Check |
|---|---|---|
| Screen dark, `i2c=none` | screen wires | GND->GND, VCC->**3V3**, SCL->22, SDA->21. SDA/SCL swapped is the classic. Wires in the same breadboard row as the pin? |
| Screen found at 0x3D | a different screen model | fine: the kit library tries 0x3C then 0x3D |
| `button=down` without touching | button legs on the same side | the two legs used must be **across** the button (diagonal is safe): one to pin 4, one to GND |
| Presses never counted | wire on wrong pin | button to **4** (labelled D4 or 4), not 2 or 5 |
| No sound | buzzer | + leg (longer, or marked +) to **23**, other to GND. An active buzzer only clicks with tones: that's the part, not the code |
| Board resets when pressing | button to 3V3 and GND shorted | rewire per docs/kit.md |
| Nothing at all, no light on the board | power/cable | another cable; is the red power LED on? |
| Flappy shows but the button does nothing | button wiring | as above |

Fix one thing, re-run the listen, repeat. When everything passes, record "kit checked" in `my_projects/PROGRESS.md`
and celebrate: the kit is now theirs to program.
