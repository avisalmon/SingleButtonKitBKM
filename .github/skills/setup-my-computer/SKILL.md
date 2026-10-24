---
name: setup-my-computer
description: >
  Get a Windows computer ready to program the Single Button kit: Python, the project's `env` virtualenv, PlatformIO
  and esptool from requirements.txt, and the CP210x USB driver. Fixes "command not found", PATH and pip trouble.
  macOS/Linux: adapts the same steps (untested by the maintainer, say so).
  TRIGGER: "set up my computer", "install", "python not found", "pio not found", "command not found", "pip error",
  "driver", "התקנה", "תתקין", "לא מוצא את פייתון", or kit-guide phase 2.
---

# Set up my computer

Goal: `.\env\Scripts\python.exe scripts\kit_doctor.py` prints no FAIL. Do every step yourself; the learner only
approves installers (Windows asks "Do you want to allow this app to make changes?": they click **Yes**).
Explain each step in one sentence ("Python is the language our helper tools are written in").

## 1. Python (3.12)

* Check: `python --version` and `py -3 --version`. **Beware** `python` that opens the Microsoft Store or prints nothing:
  that is the Windows "App execution alias", not Python (gotchas #1).
* Install if missing: `winget install --id Python.Python.3.12 -e --source winget --accept-package-agreements --accept-source-agreements`.
  Then **open a new terminal** (PATH changes only reach new ones) or call it by full path:
  `$env:LOCALAPPDATA\Programs\Python\Python312\python.exe`.
* No winget? Have the learner install from python.org, ticking **"Add python.exe to PATH"** on the first screen.

## 2. The env and the tools

```powershell
python -m venv env
.\env\Scripts\python.exe -m pip install --upgrade pip
.\env\Scripts\python.exe -m pip install -r requirements.txt
```

Always `env`, never `.venv`/`venv` (CLAUDE.md rule 2). PlatformIO downloads the ESP32 compiler (~500 MB) on the
**first build**, not here: warn the learner that the first build takes a few minutes, later ones seconds.

## 3. The USB driver (CP210x)

The kit's ESP32 board talks to USB through a Silicon Labs CP210x chip. Windows 10/11 usually installs its driver
by itself the first time the kit is plugged in.

* Check: `.\env\Scripts\python.exe scripts\kit_doctor.py`. "kit found on COMx" = done.
* "Windows sees the kit but has no driver": install it. `winget search CP210x` may find it; otherwise send the learner
  to https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers (Downloads -> **CP210x Universal Windows Driver**),
  unzip, right-click `silabser.inf` -> **Install**. Then unplug and replug the kit.
* "No kit on USB" and nothing in Device Manager: almost always a **charge-only cable** (gotchas #2). Try another
  cable, then another USB socket.
* A board with a CH340 chip instead: driver from the WCH site (wch-ic.com, CH341SER). The rest is the same.

## 4. Check

`.\env\Scripts\python.exe scripts\kit_doctor.py` -> no FAIL. Record "computer ready" in `my_projects/PROGRESS.md`.

## macOS / Linux

Same steps with `python3 -m venv env` and `env/bin/python`. No driver is needed on recent macOS/Linux for CP210x.
Linux: the user must be in the `dialout` group (`sudo usermod -aG dialout $USER`, then log out and in).
The maintainer tests on Windows only: tell the learner, and record anything you had to change with `improve-this-guide`.
