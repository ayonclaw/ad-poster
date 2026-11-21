"""Write the Shellhavn travel poster to /output/entry.png."""
import os
import shutil
from pathlib import Path

OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

POSTER = "poster.png"


def main() -> None:
    """Copy the rendered poster beside this file into the output directory."""
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().parent / POSTER, OUT / "entry.png")


if __name__ == "__main__":
    main()
