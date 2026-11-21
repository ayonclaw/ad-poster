"""Hand the Shellhavn poster to the grader as /output/entry.png."""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTDIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
ARTWORK = "poster.png"
ENTRY = "entry.png"


def publish() -> None:
    """Copy the rendered artwork into the output directory as the entry image."""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / ARTWORK, OUTDIR / ENTRY)


if __name__ == "__main__":
    publish()
