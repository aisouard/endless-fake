"""Endless Fake

Usage:
  endless-fake-playback [--offset FRAME] <video.avi>
  endless-fake-playback (-h | --help)

Options:
  -o --offset FRAME  Start the video at that frame number.
  -h --help          Show this screen.
  --version          Show version.
"""
import cv2
from docopt import docopt

from .. import version
from ..imagesource.videoimagesource import VideoImageSource
from ..renderer.pygamerenderer import PygameRenderer
from ..scanner import Scanner


def main():
    args = docopt(__doc__, version=version, options_first=True)
    offset = 0 if not args["--offset"] else int(args["--offset"])
    filename = args["<video.avi>"]

    video = VideoImageSource(filepath=filename, offset=offset)
    renderer = PygameRenderer()
    scanner = Scanner()

    while renderer.update():
        frame = video.grab_frame()
        if frame is None:
            break

        result = scanner.process(frame)

        if result is not None:
            scanner.debug_draw(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        renderer.render(frame)

    renderer.shutdown()
    video.shutdown()


if __name__ == "__main__":
    main()
