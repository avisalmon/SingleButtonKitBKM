# What we learned, by date

The short version of every lesson added to this guide, newest first. Each line points to where the full rule lives.
They come from real sessions with real kits; most of them came from something going wrong.

## 2026-10-24

- **Assume nobody has used a command line.** The start page now copies the project with clicks (Git: Clone in VS Code)
  and explains the terminal from zero for those who want it; the chat says what each command does before it runs.
  [get_started.md](get_started.md)
- **Learn by hand before the magic.** The start page's stage 2 is MicroPython with the single_button course; the chat
  expects a kit running MicroPython, and Thonny holding the port. [journey.md](journey.md)

- **The guide is born, and tested on a real kit.** Doctor, upload, kit_check, listen and Flappy restore all ran on an
  ESP32-D0WD-V3 kit. [journey.md](journey.md)
- **A listed port can still be dead.** Windows kept the CP210x stopped (Code 10) while the port showed in the list;
  the doctor now checks the device state, not only the list. [gotchas #4](gotchas.md)
- **A WiFi kit's flash holds the WiFi password.** Never publish a flash dump without checking it. [gotchas #6](gotchas.md)
- **Reading the whole flash needs a slow speed** on some kits, though writing fast works. [gotchas #5](gotchas.md)
- **One build at a time per project.** A second build of the same folder fails on a locked file. [gotchas #7](gotchas.md)
