"""Shellhavn entry: copy the poster to /output/entry.png."""
import os
import shutil

ART = "poster.png"
TARGET = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def ship() -> None:
    """Place the finished poster where the harness reads the entry."""
    folder = os.path.dirname(TARGET)
    if folder:
        os.makedirs(folder, exist_ok=True)
    shutil.copyfile(ART, TARGET)


ship()
