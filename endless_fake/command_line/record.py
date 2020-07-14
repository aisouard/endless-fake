"""Endless Fake

Usage:
  endless-fake-record --output FILE
                      [--chrome-driver PATH]
                      [--fps FPS]
                      [-x X]
                      [-y Y]
                      <game-dir>
  endless-fake-record (-h | --help)

Options:
  --chrome-driver PATH  Path to chromedriver binary.
  -f, --fps FPS         Number of frames per second, default 30.
  -o, --output FILE     Output video path.
  -x X                  Offset of the X coordinate.
  -y Y                  Offset of the Y coordinate.
  -h --help             Show this screen.
  --version             Show version.
"""
import os
import time
from docopt import docopt

from .. import version
from ..browser.seleniumbrowser import SeleniumBrowser
from ..imagesource.screencapturerimagesource import ScreenCapturerImageSource
from ..renderer.videorenderer import VideoRenderer


def main():
    args = docopt(__doc__, version=version, options_first=True)
    print(args)
    output_file = args["--output"]
    fps = 30 if not args["--fps"] else int(args["--fps"])
    chrome_driver = None if not args["--chrome-driver"] else args["--chrome-driver"]
    x = None if not args["-x"] else args["-x"]
    y = None if not args["-y"] else args["-y"]

    renderer = VideoRenderer(output_file, fps)
    screencapturer = ScreenCapturerImageSource(x_offset=x, y_offset=y)
    url = "file:///{}".format(os.path.join(os.path.abspath(args["<game-dir>"]), "index.html"))
    browser = SeleniumBrowser(url=url, chrome_driver=chrome_driver)

    while True:
        try:
            x, y = browser.get_position()
            frame = screencapturer.grab_frame(x, y)
            renderer.render(frame)
            time.sleep(1. / fps)
        except Exception:
            break

    renderer.shutdown()
    browser.shutdown()


if __name__ == "__main__":
    main()
