# Spec: SingleButtonKitBKM

## What it is

A "best known method" guide for the Single Button kit (ESP32 DevKit + SSD1306 OLED + one button + buzzer), in the spirit
of [FullStackBKM](https://github.com/avisalmon/FullStackBKM): the learner sets up an editor with an AI chat, clones this
repo and says "Tell me what to do"; from there the AI (Claude Code or GitHub Copilot) guides them, installs what is
needed, connects the kit, and builds with them whatever they imagine, teaching as it goes.

## Audience

Children, students and teachers in Israel first: Hebrew by default, English everywhere as a switch (start page) or by
writing in English (the chat). Assume no programming experience and no terminal experience.

## Pieces

* `index.html`: the public start page (GitHub Pages): the kit, the assembly video, the wiring, first steps, links to the
  hand-coding MicroPython course (github.com/avisalmon/single_button and its playlist).
* `CLAUDE.md` + 10 skills in `.claude/skills/`, mirrored to `.github/skills/` with generated
  `.github/copilot-instructions.md` and `AGENTS.md`.
* Arduino-style C++ with PlatformIO (pinned: espressif32 7.1.3 = Arduino core 2.0.17), the `SingleButtonKit` library,
  examples, a starter template, `my_projects/` (git-ignored learner space).
* Scripts: kit_doctor (read-only checks), listen (bounded serial read), new_project, restore_flappy, check_updates,
  sync_skills. Tests in `tests/`, CI builds every example.

## Decisions

* **Windows first.** The maintainer tests on Windows; macOS/Linux steps exist but are unverified and say so.
* **The learner's work never conflicts with updates**: it lives in git-ignored `my_projects/`; every session pulls.
* **Flappy can always come back**: full 4 MB images, checksum-checked before writing, checked free of WiFi credentials.
* **Pinned versions**, so a project that builds today builds next year.

## Not in scope

MicroPython lessons (they live in single_button), kits with different parts, soldering.
