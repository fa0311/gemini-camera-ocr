import asyncio
import logging
import threading

import cv2


class Camera:
    def __init__(self, cap: cv2.VideoCapture) -> None:
        self.cap = cap
        self.logger = logging.getLogger(__name__)
        self.latest = None
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    @staticmethod
    def open(index: int) -> "Camera":
        cap = cv2.VideoCapture(index)
        return Camera(cap)

    async def __aenter__(self) -> "Camera":
        if not self.cap.isOpened():
            raise RuntimeError("Camera open failed.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280 // 2)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720 // 2)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.running = True

        self.logger.info("Camera opened")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.cap.release()
        self.running = False
        self.logger.info("Camera released")

    def _loop(self):
        while self.running:
            if not self.cap.grab():
                continue
            ok, frame = self.cap.retrieve()
            if not ok:
                continue
            with self.lock:
                self.latest = frame

    def read(self):
        if self.latest is None:
            raise RuntimeError("No frame available")
        with self.lock:
            return self.latest.copy()

    async def read_frame(self, jpeg_quality: int) -> bytes:
        def callback():
            frame = self.read()

            ok, buf = cv2.imencode(
                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            )
            if not ok:
                raise RuntimeError("JPEG encode failed")
            return buf.tobytes()

        return await asyncio.to_thread(callback)
