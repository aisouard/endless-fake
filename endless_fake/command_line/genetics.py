"""Endless Fake

Usage:
  endless-fake-genetics [<args>...]
  endless-fake-genetics (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt

from .. import version


def main():
    args = docopt(__doc__, version=version, options_first=True)
    raise("Not implemented yet")


if __name__ == "__main__":
    main()
