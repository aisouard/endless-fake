import cv2


class VideoRenderer:
    def __init__(self, filename, fps):
        fourcc = cv2.VideoWriter_fourcc(*'RGBA')
        self._out = cv2.VideoWriter(filename, fourcc, fps, (360, 640))

    def update(self):
        pass

    def render(self, frame):
        self._out.write(frame)

    def shutdown(self):
        self._out.release()
