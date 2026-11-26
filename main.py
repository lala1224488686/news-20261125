"""Ship the rendered front page to the output folder.

This is the whole job of the entry point, and it deliberately uses
nothing but the Python standard library:

1. Find the entry.png that sits next to this file (render_news.py
   produces it).
2. Copy it, byte for byte, into the folder named by the
   MAKEFUN_OUTPUT_DIR environment variable, falling back to /output.
3. Make the delivered copy readable by everyone (mode 0644).

Copying a fixed file is deterministic by construction: running this
twice yields two identical files, which is easy to check by hashing.
"""

import os
import shutil

OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT = "/output"
ENTRY_NAME = "entry.png"
DELIVERED_MODE = 0o644


def entry_source():
    """Absolute path of the entry.png living next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ENTRY_NAME)


def output_folder():
    """Where the finished page goes; /output unless told otherwise."""
    return os.environ.get(OUTPUT_ENV, DEFAULT_OUTPUT)


def deliver():
    source = entry_source()
    if not os.path.isfile(source):
        raise SystemExit("missing input: %s (run render_news.py first)"
                         % source)
    folder = output_folder()
    os.makedirs(folder, exist_ok=True)
    destination = os.path.join(folder, ENTRY_NAME)
    shutil.copyfile(source, destination)
    os.chmod(destination, DELIVERED_MODE)
    print("delivered %s -> %s" % (source, destination))


if __name__ == "__main__":
    deliver()
