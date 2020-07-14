"""Endless Fake

Usage:
  endless-fake-patch [--disable-random] <game-dir>
  endless-fake-patch (-h | --help)

Options:
  --disable-random   Always output the same level.
  -h --help          Show this screen.
  --version          Show version.
"""
import os
import re
from docopt import docopt

from .. import version


def patch_files(game_dir):
    game_html = os.path.join(game_dir, "game.html")
    game_min_js = os.path.join(game_dir, "game.min.js")

    print("Patching game.html")
    with open(game_html, "r") as stream:
        data = stream.read()
    with open(game_html, "w") as stream:
        stream.write(re.sub(r"//cdn\.gameplayer\.io/api/js/", "", data))

    print("Patching game.min.js")
    with open(game_min_js, "r") as stream:
        data = stream.read()
    with open(game_min_js, "w") as stream:
        data = re.sub(r"this\.preserveDrawingBuffer=d\.preserveDrawingBuffer",
                      "this.preserveDrawingBuffer:1", data)
        data = re.sub(r"getContext\(\"webgl\"\)",
                      "getContext(\"webgl\",{preserveDrawingBuffer:true})", data)
        data = re.sub(r"getContext\(\"experimental-webgl\"\)",
                      "getContext(\"experimental-webgl\",{preserveDrawingBuffer:true})", data)
        stream.write(data)


def main():
    args = docopt(__doc__, version=version, options_first=True)
    output_dir = args["<game-dir>"]
    patch_files(output_dir)


if __name__ == "__main__":
    main()
