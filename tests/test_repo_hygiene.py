"""Things that must never land in a public repo children clone."""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def tracked_files():
    done = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True)
    return [ROOT / line for line in done.stdout.splitlines() if line]


def test_virtualenv_and_learner_work_are_ignored():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for must in ("env/", ".env", ".pio/", "my_projects/*", "!my_projects/README.md"):
        assert must in ignore.splitlines(), must
    files = {p.relative_to(ROOT).as_posix() for p in tracked_files()}
    assert not any(f.startswith(("env/", ".pio/")) or "/.pio/" in f for f in files)
    assert {f for f in files if f.startswith("my_projects/")} <= {"my_projects/README.md"}


def test_no_wifi_passwords_or_keys_in_code_or_docs():
    pattern = re.compile(
        r"""(password|passwd|pswd|api_key|apikey|secret)\s*=\s*["'][^"'.]{4,}["']""", re.I
    )
    for path in tracked_files():
        if path.suffix in (".bin", ".png") or not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not pattern.search(text), f"looks like a secret in {path.relative_to(ROOT)}"


def test_relative_links_in_docs_point_at_real_files():
    link = re.compile(r"\]\((?!https?:|mailto:|#)([^)#\s]+)")
    for md in [ROOT / "README.md", ROOT / "CLAUDE.md", *ROOT.glob("docs/*.md"), *ROOT.glob(".claude/skills/*/SKILL.md")]:
        for target in link.findall(md.read_text(encoding="utf-8")):
            assert (md.parent / target).resolve().exists(), f"{md.relative_to(ROOT)} -> {target}"
