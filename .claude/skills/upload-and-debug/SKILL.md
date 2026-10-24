---
name: upload-and-debug
description: >
  Build, upload and read the output of a PlatformIO project on the Single Button kit, and fix what goes wrong:
  compile errors, upload failures ("Failed to connect", port busy, access denied), boot loops, and programs that
  run but misbehave. Uses scripts/listen.py to read Serial without blocking.
  TRIGGER: "upload", "flash", "build", "compile", "it doesn't upload", "error", "failed to connect", "port busy",
  "nothing happens", "it keeps restarting", "read the output", "serial", "תעלה", "שגיאה", "לא עולה", "לא עובד".
---

# Upload and debug

## The loop (run it yourself, every change)

```powershell
$env:PYTHONIOENCODING="utf-8"
.\env\Scripts\pio.exe run -d my_projects\<name>                 # build only: fast, catches mistakes
.\env\Scripts\pio.exe run -d my_projects\<name> -t upload       # build + upload (finds the port itself)
.\env\Scripts\python.exe scripts\listen.py --seconds 8          # restart the kit and read what it prints
```

Several boards connected: add `--upload-port COM5` to pio and `--port COM5` to listen.
The first build of a session can take minutes (downloads, library compile); say so before starting.
Read the result from the command's output: look for `SUCCESS`, `FAILED`, `error:`.

## Never

* `pio device monitor` (never ends, holds the port, blocks the next upload; CLAUDE.md rule 9).
* Leave a `listen.py` or monitor running in the background before an upload.

## Compile errors

Read the **first** `error:` line; later ones are usually echoes. Fix, rebuild. Common ones on this kit:
* `SingleButtonKit.h: No such file`: the project's platformio.ini lost `extra_configs = ../../kit.ini` / `extends = kit`,
  or the project is not two folders below the repo root (`my_projects/<name>`).
* `'screen' was not declared`: missing `#include <SingleButtonKit.h>`.
* Hebrew or emoji in `screen.print`: the built-in font is English-only (kit-hardware: text).

## Upload errors

| Message | Fix |
|---|---|
| `Failed to connect to ESP32` / `Wrong boot mode` | learner holds **BOOT**, run again, release at "Connecting..." (gotchas #3) |
| `could not open port` / `Access is denied` / `busy` | another program has the port: a monitor, Thonny, Arduino IDE, a forgotten listen. Close it |
| `No serial port found` / `Please specify upload_port` | kit not on USB: `scripts/kit_doctor.py` |
| `UnicodeEncodeError` | `$env:PYTHONIOENCODING="utf-8"` was not set in that command |
| Timeouts mid-upload | try `--upload-port` explicitly, another cable or USB socket; `upload_speed = 115200` in the project |

## Runs but misbehaves

* **Restarts again and again** (listen shows `rst:` and boot text repeating): a crash. Common: huge arrays on the stack
  (make them `static` or global), a `while` loop that never calls `delay()` or `yield()` for seconds (watchdog), or
  dividing by zero. Strip `loop()` down until it stays up, then add back one piece at a time.
* **Screen stays black** but kit_check worked: `screen.display()` never called, or drawing off-screen (x>127, y>63).
* **Button misses presses**: a long `delay()` in `loop()`. Use `millis()` timing (kit-hardware: timing).
* **Add prints**: `Serial.printf("x=%d\n", x);` then listen. Remove them when done.

Every new trap you solve: `improve-this-guide`.
