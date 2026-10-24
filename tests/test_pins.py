"""The kit's wiring is written in three places: the library, docs/kit.md and the start page.
A pin changed in one and not the others sends a child to the wrong hole in the breadboard."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / "lib" / "SingleButtonKit" / "src" / "SingleButtonKit.h").read_text(encoding="utf-8")
EXPECTED = {"SDA": "21", "SCL": "22", "BUTTON": "4", "BUZZER": "23"}


def library_pins():
    return dict(re.findall(r"constexpr int KIT_PIN_(\w+) = (\d+);", HEADER))


def test_library_has_the_kit_wiring():
    assert library_pins() == EXPECTED


def test_kit_md_table_matches_the_library():
    text = (ROOT / "docs" / "kit.md").read_text(encoding="utf-8")
    table = text.split("<!-- pins:start")[1].split("<!-- pins:end -->")[0]
    rows = dict(re.findall(r"^\| (.+?) \| (\w+) \|$", table, re.M))
    pins = library_pins()
    assert rows["Screen SDA"] == pins["SDA"]
    assert rows["Screen SCL"] == pins["SCL"]
    assert rows["Button, one leg"] == pins["BUTTON"]
    assert rows["Buzzer +"] == pins["BUZZER"]
    assert rows["Screen VCC"] == "3V3", "the screen must never be wired to 5V"


def test_start_page_table_matches_the_library():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    table = html.split('<table id="pins">')[1].split("</table>")[0]
    rows = dict(re.findall(r'<span lang="en">([^<]+)</span></td><td><code>(\w+)</code>', table))
    pins = library_pins()
    assert rows["Screen SDA"] == pins["SDA"]
    assert rows["Screen SCL"] == pins["SCL"]
    assert rows["Button, one leg"] == pins["BUTTON"]
    assert rows["Buzzer +"] == pins["BUZZER"]
    assert rows["Screen VCC"] == "3V3"


def test_skills_quote_the_same_pins():
    for skill in ("connect-the-kit", "kit-hardware"):
        text = (ROOT / ".claude" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        for wrong in ("SDA->22", "SCL->21", "SDA 22", "SCL 21"):
            assert wrong not in text, (skill, wrong)
