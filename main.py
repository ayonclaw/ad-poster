"""Shellhavn: place the finished travel poster where the grader looks."""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESTINATION = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
FORMAT = "png"
PIXELS = 1024
NOTE = "one finished poster, no network, no build step"


def emit() -> None:
    """Copy the poster drawn beside this program to the output path."""
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "poster.png", DESTINATION)


if __name__ == "__main__":
    emit()