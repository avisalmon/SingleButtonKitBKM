# The journey: from a built kit to your own programs

Who does what in each phase. The chat (the `kit-guide` skill) leads you through it and records your progress in
`my_projects/PROGRESS.md`, so you can stop any time and say "continue" tomorrow.

## Phase 0 - Get to a working chat (you, once per computer)

The start page (index.html) and [get_started.md](get_started.md):
- [ ] VS Code installed
- [ ] Git installed
- [ ] An AI chat in VS Code: Claude Code or GitHub Copilot (Agent mode), signed in, answers "hello"
- [ ] This repo cloned and opened in VS Code
- [ ] Typed "תגיד לי מה לעשות" / "Tell me what to do"

## Phase 1 - The kit works on its own (you, with the video)

- [ ] Kit assembled following the [assembly video](https://www.youtube.com/watch?v=Jap-4eeCaNw) and [kit.md](kit.md)
- [ ] Plugged into USB: Flappy shows; the button makes the bird fly; you hear it

If not, tell the chat what you see; it checks the wiring with you (`connect-the-kit`).

## Phase 2 - The computer is ready (the chat)

- [ ] Python 3.12, the `env` folder, PlatformIO and esptool (`setup-my-computer`). You click "Yes" on installers.
- [ ] USB driver: the kit appears on a COM port
- [ ] `scripts/kit_doctor.py` shows no FAIL

## Phase 3 - The kit talks to the computer (the chat, you press the button)

- [ ] `kit_doctor.py --chip`: the ESP32 answers
- [ ] You know uploading replaces Flappy, and that it can come back any time (`restore-flappy`)
- [ ] `examples/kit_check` uploaded; you press the button; `kit_doctor.py --listen` sees screen, button and presses; you hear the beeps

## Phase 4 - Your first program (together)

- [ ] A project in `my_projects/` with your name on the screen and a beep on each press
- [ ] **You** changed something in the code (the text, the sound) and saw it change on the kit

## Phase 5 - Make anything (together, as long as you like)

- [ ] A game or gadget of your own idea ([ideas.md](ideas.md) has many), built step by step (`make-magic`)
- [ ] You can explain what your program does, and change it yourself (`kit-mentor`: "quiz me")

## You graduated when

You made a program of your own idea, you can point to the line that reads the button and the line that draws, and you
changed it yourself. Then: make the next one, teach a friend, or learn to write it all by hand (the MicroPython course
linked from the start page).

## Always

- Every session starts by pulling updates to this guide (automatic).
- Your work is in `my_projects/`, which updates never touch.
- Flappy can come back any time: "תחזיר את פלאפי" / "Restore Flappy".
