"""Shared helpers for the kit scripts: where the repo is, finding the kit's COM port, reading its serial output.

Imported by kit_doctor.py, listen.py and restore_flappy.py (they sit in the same folder).
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PYTHON = ROOT / "env" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
BAUD = 115200

# USB-to-serial chips found on ESP32 boards, by USB vendor:product id.
USB_CHIPS = {
    (0x10C4, 0xEA60): "CP210x (Silicon Labs)",  # the kit's ESP32 DevKit
    (0x1A86, 0x7523): "CH340 (WCH)",
    (0x1A86, 0x55D4): "CH9102 (WCH)",
    (0x0403, 0x6001): "FTDI FT232",
    (0x0403, 0x6015): "FTDI FT231X",
    (0x303A, 0x1001): "ESP32 built-in USB",
}


def chip_name(vid, pid):
    """The USB-to-serial chip's name, or None when the port is not an ESP32-style board."""
    if vid is None or pid is None:
        return None
    return USB_CHIPS.get((vid, pid))


def kit_ports():
    """[(device, chip name, description)] for every connected port that looks like an ESP32 board."""
    from serial.tools import list_ports

    found = []
    for port in list_ports.comports():
        name = chip_name(port.vid, port.pid)
        if name:
            found.append((port.device, name, port.description or ""))
    return found


def all_ports():
    from serial.tools import list_ports

    return [(p.device, p.description or "") for p in list_ports.comports()]


def pick_port(requested=None):
    """The port to use: the one asked for, or the single kit found. Exits with a plain message otherwise."""
    if requested:
        return requested
    ports = kit_ports()
    if len(ports) == 1:
        return ports[0][0]
    if not ports:
        sys.exit(
            "No kit found on USB. Plug it in with a cable that carries data (some only charge), "
            "then run: python scripts/kit_doctor.py"
        )
    names = ", ".join(device for device, _, _ in ports)
    sys.exit(f"More than one board is connected ({names}). Say which one with --port.")


def kitcheck_lines(lines):
    """{key: [values]} from KITCHECK lines, e.g. 'KITCHECK screen=ok addr=0x3C' -> screen: ['ok'], addr: ['0x3C']."""
    result = {}
    for line in lines:
        line = line.strip()
        if not line.startswith("KITCHECK"):
            continue
        for part in line.split()[1:]:
            key, sep, value = part.partition("=")
            if sep:
                result.setdefault(key, []).append(value)
            else:
                result.setdefault(key, []).append("")
    return result


def listen(port, seconds, reset=True, echo=True):
    """Read the kit's serial output for `seconds`. With reset, restart the board first so nothing is missed.

    Returns the lines read. Never holds the port after returning, so an upload can follow straight away.
    """
    import serial

    lines = []
    with serial.Serial(port, BAUD, timeout=0.2) as link:
        if reset:
            # EN is wired to RTS on these boards: pulse it to restart the program; keep BOOT (DTR) released.
            link.dtr = False
            link.rts = True
            time.sleep(0.1)
            link.rts = False
        end = time.monotonic() + seconds
        pending = b""
        while time.monotonic() < end:
            pending += link.read(256)
            while b"\n" in pending:
                raw, pending = pending.split(b"\n", 1)
                text = raw.decode("utf-8", errors="replace").rstrip("\r")
                lines.append(text)
                if echo:
                    print(text, flush=True)
        if pending:
            lines.append(pending.decode("utf-8", errors="replace"))
    return lines
