---
name: improve-this-guide
description: >
  Turn what went wrong (or a better way found) into a lasting improvement of this guide: a short post-mortem, a new or
  updated gotcha, skill or example, and a line in the lessons log. For learners it records a suggestion; for the
  maintainer it edits the guide, syncs the Copilot copies and runs the tests.
  TRIGGER: "that was wrong", "remember this", "add this to the guide", "this should be a lesson", "post-mortem",
  "update the skill", "תוסיף למדריך", "תזכור את זה", "זה צריך להיות לקח", or after you solved a new problem.
---

# Improve this guide

Every learner who hits a problem should be the last one to hit it. This guide improves from real sessions.

## When you are helping a learner (most sessions)

Do **not** edit the guide's files in their copy: the next update would clash with it (CLAUDE.md rule 4).
Instead, when you solved something the docs did not cover:
1. Write it in three lines in `my_projects/SUGGESTIONS.md`: what happened, why, what fixed it.
2. Tell the learner (or their teacher) that the guide's author would love it: they can open an issue at
   https://github.com/avisalmon/SingleButtonKitBKM/issues with that text (ask before doing it for them).

## When you are the maintainer's assistant (working on the guide itself)

1. **Post-mortem** in four lines: what happened; why the way we work let it happen; the rule or fix that prevents it;
   where it lives.
2. Land it where the next AI will read it at the right moment:
   * a trap -> a numbered entry in [docs/gotchas.md](../../../docs/gotchas.md) (never renumber old ones: skills point at them),
   * a behaviour -> the skill that covers it (`.claude/skills/<name>/SKILL.md`) or `CLAUDE.md`,
   * a tool gap -> the script (`scripts/kit_doctor.py` should detect anything we diagnosed by hand), with a test.
3. Add a dated line to [docs/lessons_log.md](../../../docs/lessons_log.md) (newest first, `## YYYY-MM-DD`, `- **Lesson.** pointer`).
4. `.\env\Scripts\python.exe scripts\sync_skills.py` (mirrors skills to `.github/skills/`, regenerates
   `copilot-instructions.md` and `AGENTS.md`, stamps "last updated" on README.md and index.html).
5. `.\env\Scripts\python.exe -m pytest -q` -> all pass. If examples or the library changed, build every example
   (`pio run -d examples/<each>`), and test on a real kit when hardware behaviour changed.
6. Commit with a message that says the lesson; push only when the maintainer says so. Learners receive it at their next
   session through `check_updates.py`.
