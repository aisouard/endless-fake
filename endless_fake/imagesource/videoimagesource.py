import cv2


class VideoImageSource:
    def __init__(self, filepath, offset=0):
        self._cap = cv2.VideoCapture(filepath)
        if not self._cap.isOpened():
            raise Exception("Can't open {}".format(filepath))

        count = 0
        while count < offset:
            self._cap.read()
            count += 1

    def grab_frame(self):
        if not self._cap.isOpened():
            self.shutdown()
            return None

        ret, frame = self._cap.read()
        if not ret:
            self.shutdown()
            return None

        return frame

    def shutdown(self):
        if self._cap is None:
            return

        self._cap.release()
        self._cap = None
