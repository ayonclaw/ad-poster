"""Write the finished Shellhavn travel poster to /output/entry.png."""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    """Copy the poster image the sandbox renders from."""
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "poster.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
