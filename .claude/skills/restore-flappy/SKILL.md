---
name: restore-flappy
description: >
  Put the Flappy game back on the Single Button kit exactly as it shipped (the Flappy collection, or the original
  single game), for example before handing kits to a class or after experimenting. Writes a full 4 MB image.
  TRIGGER: "restore Flappy", "bring back the game", "put Flappy back", "factory reset the kit", "original game",
  "תחזיר את פלאפי", "תחזיר את המשחק", "איפוס", "להחזיר את הערכה למצב המקורי".
---

# Restore Flappy

1. Tell the learner what will happen: the program now on the kit is replaced by Flappy; their projects stay safe in
   `my_projects/` and can be uploaded again any time. Ask "OK?" if they have not asked for it in so many words.
2. Run (the kit must be connected, no serial monitor open):

   ```powershell
   $env:PYTHONIOENCODING="utf-8"; .\env\Scripts\python.exe scripts\restore_flappy.py
   ```

   `--original` for the original single game instead of the collection. Takes about a minute.
   The script checks the image's checksum first and refuses a damaged file.
3. "Failed to connect": the learner holds **BOOT** (right of the USB socket) while you run it again, and lets go when
   "Connecting..." appears. "Packet content transfer stopped" or timeouts: run again with `--baud 115200`.
4. Ask them to look: Flappy's title screen should appear; a press starts the game.
5. Note it in `my_projects/PROGRESS.md`.

## Teachers preparing a class set

For each kit: plug in -> `scripts/kit_doctor.py --chip` -> upload `examples/kit_check` and run `kit_doctor.py --listen 20`
while pressing the button -> `restore_flappy.py` -> next kit. Offer to do this as a loop, asking the teacher to swap kits.

## Where the images came from

`firmware/flappy/` holds full flash reads from working kits (collection and original), checked to contain no WiFi
names or passwords. Never add a flash dump from a kit that has used WiFi without that check (gotchas #6).
