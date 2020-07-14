"""Endless Fake

Usage:
  endless-fake <command> [<args>...]
  endless-fake (-h | --help)
  endless-fake (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.

Commands:
  evaluate      Evaluate a previously trained machine learning model.
  fetch         Download a copy of the Endless Lake video game.
  genetics      Run a genetics algorithm to let the computer learn by itself.
  patch         Patch a copy of the video game.
  playback      Play a previously recorded gameplay video.
  record        Start a web browser and record a gameplay video.
  restore       Revert the initial backup of the video game.
  teach         Write a CSV file containing inputs and expected outputs.
  train         Train a machine learning model from a CSV file.
"""
import os
import sys
from subprocess import call
from docopt import docopt


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def main():
    args = docopt(__doc__, version="0.1.0", options_first=True)

    commands = [
        "evaluate",
        "fetch",
        "genetics",
        "patch",
        "playback",
        "record",
        "restore",
        "teach",
        "train",
        "help"
    ]

    if args["<command>"] not in commands:
        exit("{} is not an endless_fake command. See \"endless_fake help\".".format(args["<command>"]))
    elif args["<command>"] == "help":
        exit(call([sys.argv[0], "--help"]))
    else:
        exit(call(["endless-fake-{}".format(args["<command>"])] + args["<args>"]))


if __name__ == "__main__":
    main()
