# Maintaining the guide

Learners pull this repo at the start of every session, so whatever lands on `main` reaches them the next day.

## Set up

```powershell
python -m venv env
.\env\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Change something

1. Edit the source: `CLAUDE.md`, `.claude/skills/<name>/SKILL.md`, `docs/`, `lib/`, `examples/`, `index.html`.
   Never edit `.github/skills/`, `.github/copilot-instructions.md` or `AGENTS.md` by hand: they are generated.
2. A lesson learned? Add it to `docs/lessons_log.md` (newest first) and to the gotcha/skill it belongs to
   (`improve-this-guide` skill).
3. `.\env\Scripts\python.exe scripts\sync_skills.py` (mirrors skills, regenerates instructions, stamps "last updated").
4. `.\env\Scripts\python.exe -m pytest -q`.
5. Library or examples changed: build them all; hardware behaviour changed: run kit_check on a real kit.

   ```powershell
   $env:PYTHONIOENCODING="utf-8"; foreach ($e in Get-ChildItem examples -Directory) { .\env\Scripts\pio.exe run -d $e.FullName }
   ```

6. Commit, push. CI runs the tests and builds every example. GitHub Pages republishes `index.html` within a minute or two.

## Versions

Pinned in `requirements.txt` and `kit.ini`. To move up: change one version, build every example, run kit_check on a kit,
then commit with the reason. Prefer versions that have been out for at least two weeks.
