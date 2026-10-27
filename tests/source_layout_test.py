"""Check build inputs after the upstream 2D directory migration."""

from pathlib import Path
import subprocess
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("config_name", ["all", "noflags"])
def test_colrv1_source_files_exist(config_name):
    config_path = ROOT / "colrv1" / f"{config_name}.toml"
    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)
    sources = config["master"]["regular"]["srcs"]
    assert sources, "COLRv1 needs SVG source files"
    missing = [src for src in sources if not (config_path.parent / src).is_file()]
    assert not missing, f"Missing COLRv1 inputs: {missing}"


def test_bitmap_makefile_finds_emoji_sources():
    result = subprocess.run(
        ["make", "--no-print-directory", "-s", "print-EMOJI_NAMES"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    _, names = result.stdout.split("=", 1)
    actual = set(names.split())
    expected = {path.name for path in (ROOT / "2D" / "png" / "128").glob("emoji_u*.png")}
    assert expected, "Bitmap build needs PNG source files"
    assert actual == expected
