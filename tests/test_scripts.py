"""The scripts the chat relies on: they must say the right thing when the kit is missing, busy or misbehaving."""

import hashlib
from pathlib import Path

import kitlib
import new_project
import pytest
import restore_flappy

ROOT = Path(__file__).resolve().parent.parent


def test_the_kits_usb_chip_is_recognised():
    assert kitlib.chip_name(0x10C4, 0xEA60).startswith("CP210x")
    assert kitlib.chip_name(0x1A86, 0x7523).startswith("CH340")
    assert kitlib.chip_name(0x046D, 0xC52B) is None  # a mouse receiver is not a kit
    assert kitlib.chip_name(None, None) is None  # built-in serial ports have no USB ids


def test_kitcheck_report_is_parsed():
    lines = [
        "ets Jun  8 2016 00:22:57",
        "KITCHECK start",
        "KITCHECK i2c=0x3C",
        "KITCHECK screen=ok addr=0x3C",
        "KITCHECK button=up",
        "KITCHECK press=1",
        "KITCHECK press=2",
    ]
    found = kitlib.kitcheck_lines(lines)
    assert "start" in found
    assert found["screen"] == ["ok"] and found["addr"] == ["0x3C"]
    assert found["press"] == ["1", "2"]
    assert found["button"] == ["up"]


def test_kit_check_prints_what_the_doctor_reads():
    """The doctor parses kit_check's Serial lines; if one side renames a key, the check silently passes nothing."""
    source = (ROOT / "examples" / "kit_check" / "src" / "main.cpp").read_text(encoding="utf-8")
    for key in ("KITCHECK start", "KITCHECK i2c=", "KITCHECK screen=ok", "KITCHECK screen=missing",
                "KITCHECK button=", "KITCHECK press="):  # fmt: skip
        assert key in source, key


def test_new_project_creates_a_buildable_layout(tmp_path):
    target = new_project.create("space_cat", projects=tmp_path)
    ini = (target / "platformio.ini").read_text(encoding="utf-8")
    main = (target / "src" / "main.cpp").read_text(encoding="utf-8")
    assert "extra_configs = ../../kit.ini" in ini and "extends = kit" in ini
    assert "{{NAME}}" not in ini + main and "space_cat" in main
    assert "#include <SingleButtonKit.h>" in main


@pytest.mark.parametrize("bad", ["Space Cat", "חתול", "1cat", "a", "../escape", "cat-jump"])
def test_new_project_refuses_names_tools_choke_on(tmp_path, bad):
    with pytest.raises(ValueError):
        new_project.create(bad, projects=tmp_path)


def test_new_project_never_overwrites(tmp_path):
    new_project.create("mine", projects=tmp_path)
    with pytest.raises(FileExistsError):
        new_project.create("mine", projects=tmp_path)


@pytest.mark.parametrize("which", ["collection", "original"])
def test_flappy_images_match_their_checksums(which):
    name, expected = restore_flappy.IMAGES[which]
    data = (restore_flappy.FIRMWARE / name).read_bytes()
    assert len(data) == 4 * 1024 * 1024, "a full 4 MB flash image, written from address 0"
    assert hashlib.sha256(data).hexdigest() == expected


@pytest.mark.parametrize("which", ["collection", "original"])
def test_flappy_images_hold_no_wifi_settings(which):
    """A kit that joined WiFi keeps the network name and password in NVS (gotchas #6)."""
    name, _ = restore_flappy.IMAGES[which]
    nvs = (restore_flappy.FIRMWARE / name).read_bytes()[0x9000:0xE000]
    for key in (b"sta.ssid", b"sta.pswd", b"ap.ssid", b"bssid"):
        assert key not in nvs, (name, key)


def test_check_updates_points_at_this_repo():
    import check_updates

    assert check_updates.GUIDE_URL == "https://github.com/avisalmon/SingleButtonKitBKM"
    assert check_updates.normalise("https://github.com/avisalmon/SingleButtonKitBKM.git/") == check_updates.GUIDE_URL
