import nativecap
import numpy as np
import platform


class ScreenCapturerImageSource:
    def __init__(self, x_offset=None, y_offset=None):
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._platform = platform.system()

        if self._x_offset is not None and self._y_offset is not None:
            return

        if self._platform == "Windows":
            self._x_offset = 8 if not x_offset else x_offset
            self._y_offset = 124 if not y_offset else y_offset
        elif self._platform == "Linux":
            self._x_offset = 4 if not x_offset else x_offset
            self._y_offset = 127 if not y_offset else y_offset
        elif self._platform == "Darwin":
            self._x_offset = 0 if not x_offset else x_offset
            self._y_offset = 123 if not y_offset else y_offset
        else:
            raise("Unsupported platform {}".format(self._platform))

    def grab_frame(self, x, y):
        x += self._x_offset
        y += self._y_offset

        buffer = nativecap.capture(x, y, 360, 640)
        data = np.ctypeslib.as_array(buffer)
        data = data.reshape(640, 360, 4)[:, :, :3]

        return data if self._platform != "Windows" else np.flip(data, 0)

    def shutdown(self):
        pass
