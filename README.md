# SingleButtonKitBKM

### Build a kit with your hands, then program it with an AI by your side.

<!-- last-updated:start -->
**Last updated 24 October 2026** · 7 new lessons · [See what's new](docs/lessons_log.md)
<!-- last-updated:end -->

**Start page (Hebrew / English): https://avisalmon.github.io/SingleButtonKitBKM/**

---

The **Single Button kit** is an ESP32 board, a 128x64 OLED screen, one push-button and a buzzer on a breadboard.
You build it by following [a video](https://www.youtube.com/watch?v=Jap-4eeCaNw), and it starts up running a Flappy game.

This repo is what comes next. Open it in VS Code with **Claude Code** or **GitHub Copilot** (Agent mode), type
**"Tell me what to do"** (or **"תגיד לי מה לעשות"**), and the chat:

* installs what is missing on your computer (Python, PlatformIO, the USB driver),
* finds the kit, checks its screen, button and buzzer,
* builds with you whatever you imagine (games, music, timers, internet clocks), uploads it, fixes what breaks,
* teaches as it goes, in Hebrew or English, and resumes where you stopped next time,
* pulls the newest version of this guide at the start of every session.

## Three stages

1. **Build the kit** and see Flappy run: [video](https://www.youtube.com/watch?v=Jap-4eeCaNw), wiring in [docs/kit.md](docs/kit.md).
2. **Learn to program it by hand**, old school, in MicroPython: the
   [video lessons](https://www.youtube.com/playlist?list=PL0zMMCdiaE56wAuAqmGXPQlCa_2BCWRi6) and
   [the code](https://github.com/avisalmon/single_button).
3. **The AI magic** (this repo), no command-line experience needed:
   1. Install [VS Code](https://code.visualstudio.com), [Git](https://git-scm.com/downloads), and an AI chat in VS Code
      (Claude Code, or GitHub Copilot in Agent mode).
   2. In VS Code: **Ctrl+Shift+P** -> **Git: Clone** -> paste `https://github.com/avisalmon/SingleButtonKitBKM.git` ->
      pick a folder -> **Open**.
   3. In the chat, type: `Tell me what to do` / `תגיד לי מה לעשות`

Every click, and what a terminal is if you want one, is in [docs/get_started.md](docs/get_started.md).
The whole road is [docs/journey.md](docs/journey.md).

## What's in the box

```
index.html                 The start page (GitHub Pages), Hebrew + English
CLAUDE.md                  The AI's standing rules for this repo
.claude/skills/            10 playbooks: kit-guide, setup-my-computer, connect-the-kit, upload-and-debug, make-magic,
                           kit-hardware, kit-mentor, restore-flappy, share-my-project, improve-this-guide
.github/skills/            The same playbooks for GitHub Copilot (generated, kept identical by a test)
.github/copilot-instructions.md, AGENTS.md   Generated instructions + an index of every skill
lib/SingleButtonKit/       The kit library: pins, screen, debounced button, beep and tunes
kit.ini                    Shared, pinned PlatformIO settings for every project
examples/                  kit_check (proves the wiring), hello_screen, button_beep, jump_game
templates/starter/         What a new project starts from
my_projects/               YOUR work (git-ignored, so updates never touch it)
firmware/flappy/           Flappy images to restore the kit as it shipped
scripts/                   kit_doctor, listen, new_project, restore_flappy, check_updates, sync_skills
docs/                      The kit, the journey, ideas, gotchas, what's new
```

## By hand, without the AI

```powershell
python -m venv env                                   # the virtualenv is always the folder `env`
.\env\Scripts\python.exe -m pip install -r requirements.txt
.\env\Scripts\python.exe scripts\kit_doctor.py --chip
$env:PYTHONIOENCODING="utf-8"; .\env\Scripts\pio.exe run -d examples\kit_check -t upload
.\env\Scripts\python.exe scripts\kit_doctor.py --listen 20     # press the button meanwhile
.\env\Scripts\python.exe scripts\new_project.py my_game
.\env\Scripts\python.exe scripts\restore_flappy.py             # Flappy back
```

Prefer MicroPython and learning every line by hand? Avi Salmon's course for this same kit:
[github.com/avisalmon/single_button](https://github.com/avisalmon/single_button) and its
[YouTube playlist](https://www.youtube.com/playlist?list=PL0zMMCdiaE56wAuAqmGXPQlCa_2BCWRi6).

## Honest status

Tested on Windows 11 with a real kit: setup, kit_doctor, uploading kit_check, reading its report (screen, button and
buzzer confirmed by eye and ear), and writing the Flappy image (verified by esptool) all ran end to end. Not yet tested: GitHub Copilot end to end, a clean computer with nothing installed,
macOS/Linux. See [docs/backlog.md](docs/backlog.md).

## License

[MIT](LICENSE). Use it, change it, teach with it.
