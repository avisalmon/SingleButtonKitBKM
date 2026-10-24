#!/usr/bin/env python
"""Show what the kit prints on Serial for a few seconds, then let go of the port.

    python scripts/listen.py                 # restart the kit and listen for 10 seconds
    python scripts/listen.py --seconds 30 --no-reset
    python scripts/listen.py --port COM5

Use this instead of `pio device monitor` when the chat needs to read the output: a monitor never ends,
holds the port, and blocks the next upload.
"""

import argparse
import sys

from kitlib import listen, pick_port


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--port", help="COM port (found automatically when one kit is connected)")
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--no-reset", action="store_true", help="do not restart the kit first")
    args = parser.parse_args(argv)
    port = pick_port(args.port)
    print(f"--- listening on {port} for {args.seconds:g}s ---", flush=True)
    try:
        listen(port, args.seconds, reset=not args.no_reset)
    except Exception as error:  # serial errors carry the useful text ("Access is denied" = port busy)
        sys.exit(f"Could not open {port}: {error}\nIs another program (a serial monitor, Thonny) using it?")
    print("--- done ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
