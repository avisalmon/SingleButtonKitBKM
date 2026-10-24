"""The start page is the link that goes to people. Hebrew is the default and every piece of text must exist in English
too: the language switch hides one of each pair, so a missing twin is a hole in the page."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class Pairs(HTMLParser):
    """Records, for each element with lang="he", the lang of the next element at the same depth."""

    def __init__(self):
        super().__init__()
        self.depth = 0
        self.waiting = {}  # depth -> True when the previous sibling at that depth was lang="he"
        self.unpaired = []
        self.he = 0

    def handle_starttag(self, tag, attrs):
        lang = dict(attrs).get("lang")
        if self.depth in self.waiting:
            if lang != "en":
                self.unpaired.append(self.getpos())
            del self.waiting[self.depth]
        if lang == "he" and tag != "html":
            self.he += 1
            self.waiting[self.depth] = True
        if tag not in ("img", "br", "meta", "link", "input", "source"):
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in ("img", "br", "meta", "link", "input", "source"):
            return
        # The parent closes while its last child was Hebrew with no English after it.
        if self.waiting.pop(self.depth, None):
            self.unpaired.append(self.getpos())
        self.depth -= 1


def test_every_hebrew_text_has_an_english_twin():
    parser = Pairs()
    parser.feed(HTML)
    assert parser.he > 40, "the page should be bilingual throughout"
    assert parser.unpaired == [], f"Hebrew text without an English twin right after it, at (line, col): {parser.unpaired}"


def test_hebrew_is_the_default():
    assert '<html lang="he" dir="rtl" class="he">' in HTML
    assert 'setLang(wanted || "he"' in HTML


def test_the_page_carries_the_journey():
    for must in (
        "youtube-nocookie.com/embed/Jap-4eeCaNw",  # the assembly video
        "assets/wiring.png",
        "git clone https://github.com/avisalmon/SingleButtonKitBKM.git",
        "תגיד לי מה לעשות",
        "Tell me what to do",
        "github.com/avisalmon/single_button",  # learn by hand
        "PL0zMMCdiaE56wAuAqmGXPQlCa_2BCWRi6",  # the MicroPython playlist
        "code.visualstudio.com",
        "git-scm.com",
    ):
        assert must in HTML, must


def test_local_images_exist():
    import re

    for src in re.findall(r'src="(assets/[^"]+)"', HTML):
        assert (ROOT / src).exists(), src


def test_language_choice_survives_blocked_storage():
    """Private windows and some school browsers throw on localStorage: the page must still work."""
    import re

    calls = re.findall(r"localStorage\.\w+", HTML)
    guarded = re.findall(r"try \{[^}]*localStorage\.\w+", HTML)
    assert calls and len(guarded) == len(calls)
