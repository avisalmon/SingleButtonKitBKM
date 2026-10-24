# Gotchas: traps we actually hit, numbered

Skills point at these numbers: add new ones at the end, never renumber.

1. **`python` opens the Microsoft Store, or prints nothing.** That is Windows' "App execution alias", not Python.
   Install real Python (setup-my-computer) and open a **new** terminal; or call it by full path.
2. **No COM port, nothing happens when the kit is plugged in.** Most often a charge-only USB cable: it powers the board
   (the red LED lights) but carries no data. Try another cable, then another USB socket.
3. **"Failed to connect to ESP32" / "Wrong boot mode".** The automatic switch into upload mode did not work. Hold the
   **BOOT** button (right of the USB socket), start the upload, release when "Connecting..." appears.
4. **The port is listed but cannot be opened: "port is busy or doesn't exist" (FileNotFoundError), and Device Manager
   shows the CP210x with a warning (Code 10).** Seen on a real kit with the 2018 CP210x driver 6.7.6. Unplug, wait
   5 seconds, plug back in. If it keeps coming back, install the current CP210x Universal driver from Silicon Labs.
   `kit_doctor.py` detects this.
5. **Reading the whole flash (4 MB) stops with "Packet content transfer stopped"** at 460800 and at 230400 baud on the
   same kit where writing at 460800 works. Read at 115200, or read only the part you need.
6. **A flash dump of a kit that has used WiFi contains the WiFi name and password.** The ESP32 saves WiFi settings in
   its flash (the NVS area at 0x9000). Never publish a dump without checking that area; the Flappy images here were checked.
7. **Two builds of the same project at once fail with "The process cannot access the file because it is being used by
   another process".** One build at a time per project; if it happens, just build again.
8. **`UnicodeEncodeError` during upload on Windows.** Set `PYTHONIOENCODING=utf-8` for the `pio`/`esptool` command.
9. **The first build takes minutes and prints a lot.** PlatformIO downloads the ESP32 compiler (~500 MB) once.
   Later builds take seconds.
10. **The screen shows nothing although the code draws.** Drawing goes to memory; `screen.display()` sends it to the screen.
11. **The button misses presses.** A long `delay()` in `loop()`: the program is asleep while you press. Time with `millis()`.
12. **`pio device monitor` freezes the chat and blocks the next upload.** It never ends and holds the port. Use
    `scripts/listen.py`, which reads for a few seconds and lets go.
13. **Hebrew text shows as nothing or garbage.** The built-in font is English-only. Use the Hebrew recipe in the
    `kit-hardware` skill (U8g2 fonts, letters reversed for right-to-left).
