#!/usr/bin/env python3
"""news-image-20261127 — Sum up 27 November 2026 world news in one image.

The finished newspaper front page (1024x1024 PNG) is pre-rendered and
stored in this repository as entry.png. This program only copies that
file to the grader output directory.

Standard library only: no third-party imports, no network, no
randomness, no timestamps. Two runs produce byte-identical output.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main():
    # Output directory comes from the environment, defaulting to /output.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

    # The source image lives next to this program file, in the repo.
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(src):
        print("error: source image not found: %s" % src, file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(src, dst)
    print("wrote %s" % dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
