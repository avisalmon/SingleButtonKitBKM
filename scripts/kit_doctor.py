#!/usr/bin/env python
"""Check that this computer and the kit are ready, and say exactly what to fix. Read-only: changes nothing.

    python scripts/kit_doctor.py              # the computer: Python, env, tools, the kit on USB
    python scripts/kit_doctor.py --chip       # + ask the ESP32 itself what it is (chip, flash, MAC)
    python scripts/kit_doctor.py --listen 20  # + read the kit_check program's report while you press the button

Each line is OK, WARN or FAIL. Exit code 0 = no FAIL.
The chat runs this at the start, after setup, and whenever something does not work.
"""

import argparse
import importlib.metadata
import platform
import subprocess
import sys

import kitlib

results = []


def report(level, what, fix=""):
    results.append(level)
    line = f"{level:4}  {what}"
    if fix:
        line += f"\n      -> {fix}"
    print(line, flush=True)


def check_computer():
    system = platform.system()
    if system == "Windows":
        report("OK", f"Windows {platform.release()} ({platform.machine()})")
    else:
        report("WARN", f"{system}: this guide is tested on Windows; the chat will adapt the steps")

    if sys.version_info >= (3, 10):
        report("OK", f"Python {platform.python_version()}")
    else:
        report("FAIL", f"Python {platform.python_version()} is too old", "install Python 3.12 (setup-my-computer)")

    if kitlib.Path(sys.prefix).resolve() == (kitlib.ROOT / "env").resolve():
        report("OK", "running inside the project's env")
    elif kitlib.ENV_PYTHON.exists():
        report("WARN", "env exists but this run is outside it", f"run with {kitlib.ENV_PYTHON}")
    else:
        report("FAIL", "no env folder yet", "python -m venv env, then env's pip install -r requirements.txt")

    for package in ("platformio", "esptool", "pyserial"):
        try:
            report("OK", f"{package} {importlib.metadata.version(package)}")
        except importlib.metadata.PackageNotFoundError:
            report("FAIL", f"{package} is not installed in this Python", "pip install -r requirements.txt (inside env)")


def windows_usb_problems():
    """Devices Windows sees but cannot use (no driver). Empty when fine or not on Windows."""
    if platform.system() != "Windows":
        return []
    command = (
        "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'VID_10C4|VID_1A86|VID_0403' "
        "-and $_.Status -ne 'OK' } | ForEach-Object { $code = (Get-PnpDeviceProperty -InstanceId $_.InstanceId "
        "-KeyName DEVPKEY_Device_ProblemCode).Data; $_.FriendlyName + ' | ' + $_.Status + ' | code ' + $code }"
    )
    try:
        done = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    return [line for line in done.stdout.splitlines() if line.strip()]


def check_usb():
    try:
        ports = kitlib.kit_ports()
    except ImportError:
        report("FAIL", "cannot look for the kit: pyserial missing")
        return None
    problems = windows_usb_problems()
    if problems:
        # Seen on a real kit: the port is listed, but Windows has the device stopped with code 10, and opening it
        # fails with "port is busy or doesn't exist". Replugging clears it; if it keeps coming back, the driver is old.
        report("FAIL", "Windows has the kit's USB chip stopped: " + "; ".join(problems),
               "unplug the kit, wait 5 seconds, plug it back in. If it happens again: update the CP210x driver "
               "(setup-my-computer step 3, gotchas #4)")
        return None
    if len(ports) == 1:
        device, chip, _ = ports[0]
        report("OK", f"kit found on {device} ({chip})")
        return device
    if len(ports) > 1:
        report("WARN", "several boards connected: " + ", ".join(f"{d} ({c})" for d, c, _ in ports),
               "unplug the others, or pass --port")
        return None
    others = kitlib.all_ports()
    seen = f" (other ports: {', '.join(d for d, _ in others)})" if others else ""
    report("FAIL", "no kit on USB" + seen,
           "plug it in; try another cable (many only charge) and another USB socket")
    return None


def check_chip(port):
    command = [sys.executable, "-m", "esptool", "--port", port, "flash-id"]
    done = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = done.stdout + done.stderr
    if done.returncode != 0:
        lowered = text.lower()
        if "filenotfounderror" in lowered or "cannot find the file" in lowered:
            # esptool says "busy or doesn't exist"; this variant means the port vanished or the device is stopped
            report("FAIL", f"{port} is listed but cannot be opened",
                   "unplug the kit, wait 5 seconds, plug it back in, run this again")
        elif "busy" in lowered or "access is denied" in lowered or "permission" in lowered:
            report("FAIL", f"{port} is busy", "close any serial monitor, Thonny or Arduino IDE, then try again")
        else:
            report("FAIL", "the ESP32 did not answer",
                   "hold BOOT (right of the USB socket), run again, release when it says Connecting (gotchas #3)")
        return
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(("Chip is", "Chip type", "MAC", "Detected flash size", "Flash size")):
            report("OK", line)


def check_listen(port, seconds):
    print(f"\nListening to the kit for {seconds:g}s. Press the button a few times now.", flush=True)
    try:
        lines = kitlib.listen(port, seconds, reset=True, echo=False)
    except Exception as error:
        report("FAIL", f"could not open {port}: {error}", "close any serial monitor and try again")
        return
    found = kitlib.kitcheck_lines(lines)
    if "start" not in found:
        report("FAIL", "no report from the kit",
               "upload examples/kit_check first: pio run -d examples/kit_check -t upload")
        return
    devices = found.get("i2c", [])
    if found.get("screen") == ["ok"]:
        report("OK", f"screen answers at {found.get('addr', ['?'])[0]}")
    elif devices == ["none"]:
        report("FAIL", "screen: nothing answers on SDA 21 / SCL 22",
               "check the 4 screen wires: GND-GND, VCC-3V3, SCL-22, SDA-21; SDA and SCL swapped is the usual one")
    else:
        report("FAIL", f"screen not found; I2C devices seen: {', '.join(devices)}", "see docs/kit.md")
    if found.get("button") == ["down"]:
        report("FAIL", "button reads pressed without being touched",
               "the button legs go to pin 4 and GND, across the button (docs/kit.md)")
    presses = found.get("press", [])
    if presses:
        report("OK", f"button works ({len(presses)} press{'es' if len(presses) != 1 else ''} seen)")
    else:
        report("WARN", "no button presses seen",
               "press it during the listen; if it never counts, check pin 4 and GND (docs/kit.md)")
    print("      The buzzer: did you hear three rising notes at the start, and a beep per press? "
          "If not, check buzzer + to pin 23 and - to GND.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--port", help="COM port (found automatically when one kit is connected)")
    parser.add_argument("--chip", action="store_true", help="ask the ESP32 what it is")
    parser.add_argument("--listen", type=float, metavar="SECONDS", help="read kit_check's report")
    args = parser.parse_args(argv)

    print("Kit doctor\n----------")
    check_computer()
    port = args.port or check_usb()
    if port and args.chip:
        check_chip(port)
    if port and args.listen:
        check_listen(port, args.listen)
    failed = results.count("FAIL")
    print(f"\n{failed} FAIL, {results.count('WARN')} WARN" if failed else "\nAll good.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
