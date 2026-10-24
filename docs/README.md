# The documentation, and where each thing lives

## For the learner

| File | What it is |
|---|---|
| [../index.html](../index.html) | The start page (Hebrew and English): the kit, the video, the first steps |
| [get_started.md](get_started.md) | From zero to a chat that guides you, step by step |
| [kit.md](kit.md) | The kit: parts, wiring, pins, safety |
| [journey.md](journey.md) | The whole road, phase by phase, who does what |
| [ideas.md](ideas.md) | Things to make with one button, a screen and a buzzer |
| [gotchas.md](gotchas.md) | Traps we actually hit, numbered, and their fixes |
| [lessons_log.md](lessons_log.md) | What's new in this guide, by date |

## For the AI (and anyone curious)

| Where | What |
|---|---|
| [../CLAUDE.md](../CLAUDE.md) | Standing rules and which skill to use when |
| `../.claude/skills/` | The playbooks (Claude Code); `../.github/skills/` is the identical copy for GitHub Copilot |
| [../lib/SingleButtonKit/src/SingleButtonKit.h](../lib/SingleButtonKit/src/SingleButtonKit.h) | The kit library: pins, screen, button, sound |
| `../examples/` | kit_check, hello_screen, button_beep, jump_game |
| `../scripts/` | kit_doctor, listen, new_project, restore_flappy, check_updates, sync_skills |

## For the maintainer

| File | What it is |
|---|---|
| [spec.md](spec.md) | What this guide is and is not |
| [backlog.md](backlog.md) | What's next |
| [maintainer.md](maintainer.md) | How to change the guide safely: skills sync, tests, builds, publishing |
