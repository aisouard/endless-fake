"""Endless Fake

Usage:
  endless-fake-restore <path>
  endless-fake-restore (-h | --help)

Options:
  -h --help          Show this screen.
  --version          Show version.
"""
import os
from docopt import docopt

from .. import version


def restore_files(game_dir):
    game_html = os.path.join(game_dir, "game.html")
    game_html_orig = os.path.join(game_dir, "game.html.orig")
    game_min_js = os.path.join(game_dir, "game.min.js")
    game_min_js_orig = os.path.join(game_dir, "game.min.js.orig")

    print("Restoring game.html")
    with open(game_html_orig, "r") as stream:
        data = stream.read()
    with open(game_html, "w") as stream:
        stream.write(data)

    print("Restoring game.min.js")
    with open(game_min_js_orig, "r") as stream:
        data = stream.read()
    with open(game_min_js, "w") as stream:
        stream.write(data)


def main():
    args = docopt(__doc__, version=version, options_first=True)
    output_dir = os.path.join(os.getcwd(), "endlesslake") if not args["<path>"] else args["<path>"]
    restore_files(output_dir)


if __name__ == "__main__":
    main()
