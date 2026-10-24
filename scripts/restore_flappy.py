#!/usr/bin/env python
"""Put the Flappy game back on the kit, exactly as it shipped. Erases whatever program is on it now.

    python scripts/restore_flappy.py              # the Flappy collection (the default)
    python scripts/restore_flappy.py --original   # the original single Flappy game
    python scripts/restore_flappy.py --port COM5

The images are full 4 MB copies of a kit's flash, read from working kits, written from address 0.
Your projects in my_projects/ are on the computer and are not touched; upload one again any time.
"""

import argparse
import hashlib
import subprocess
import sys

from kitlib import ROOT, pick_port

FIRMWARE = ROOT / "firmware" / "flappy"
IMAGES = {
    "collection": (
        "flappy_collection.bin",
        "344357a508a437a0434b2d41a27dbe9631f8b3622328f3fc2f064d3089c28141",
    ),
    "original": (
        "flappy_original.bin",
        "4bc401ffc657bf042fbb8200952d110e23f24f122fe4f8d476000057db4dcbc6",
    ),
}


def image_path(which):
    """The image file, after proving it is the exact file we tested (a damaged image can leave the kit dead)."""
    name, expected = IMAGES[which]
    path = FIRMWARE / name
    if not path.exists():
        sys.exit(f"{path} is missing. Pull the latest version of this repo (git pull).")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        sys.exit(f"{path.name} is damaged (checksum differs). Restore it with: git checkout -- {path.relative_to(ROOT)}")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--original", action="store_true", help="the original Flappy instead of the collection")
    parser.add_argument("--port", help="COM port (found automatically when one kit is connected)")
    parser.add_argument("--baud", type=int, default=460800)
    args = parser.parse_args(argv)

    path = image_path("original" if args.original else "collection")
    port = pick_port(args.port)
    print(f"Writing {path.name} to the kit on {port}. Takes about a minute; do not unplug.", flush=True)
    command = [
        sys.executable, "-m", "esptool", "--chip", "esp32", "--port", port, "--baud", str(args.baud),
        "write-flash", "0x0", str(path),
    ]  # fmt: skip
    done = subprocess.run(command)
    if done.returncode != 0:
        print(
            "\nIt did not work. Most often: hold the BOOT button (right of the USB socket) and run this again, "
            "releasing it when 'Connecting...' appears. Also close any serial monitor using the port."
        )
        return done.returncode
    print("\nDone. The kit restarts into Flappy. Press the button to play.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
