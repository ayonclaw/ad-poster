"""Deliver the Shellhavn artwork to the grading harness."""
import os
import shutil
import sys

SOURCE_NAME = "poster.png"
OUTPUT_NAME = "entry.png"


def output_folder() -> str:
    """Return the directory the harness collects the entry from."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def deliver(artwork: str, folder: str) -> None:
    """Copy the artwork into the folder as the entry image."""
    os.makedirs(folder, exist_ok=True)
    shutil.copyfile(artwork, os.path.join(folder, OUTPUT_NAME))


def run() -> int:
    """Place the poster and report the size written."""
    home = os.path.dirname(os.path.abspath(__file__))
    folder = output_folder()
    deliver(os.path.join(home, SOURCE_NAME), folder)
    written = os.path.join(folder, OUTPUT_NAME)
    sys.stderr.write("wrote %s (%d bytes)\n" % (written, os.path.getsize(written)))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
