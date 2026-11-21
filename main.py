"""Shellhavn, the drowned harbour: hand the finished poster to the grader."""
import os
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent
POSTER = REPO / "poster.png"
TARGET_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = TARGET_DIR / "entry.png"
IMAGE_SUFFIX = ".png"
IMAGE_IS_OPAQUE = True


def render() -> None:
    """Place the rendered poster at the path the harness reads."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(POSTER, TARGET)


if __name__ == "__main__":
    render()
