import asyncio
import logging

import cv2


class Camera:
    def __init__(self, cap: cv2.VideoCapture) -> None:
        self.cap = cap
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def open(index: int) -> "Camera":
        cap = cv2.VideoCapture(index)
        return Camera(cap)

    async def __aenter__(self) -> "Camera":
        if not self.cap.isOpened():
            raise RuntimeError("Camera open failed.")
        self.logger.info("Camera opened")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.cap.release()
        self.logger.info("Camera released")

    async def read_frame(self, jpeg_quality: int) -> bytes:
        def callback():
            ok, frame = self.cap.read()
            if not ok or frame is None:
                raise RuntimeError("Frame read failed.")

            ok, buf = cv2.imencode(
                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            )
            if not ok:
                raise RuntimeError("JPEG encode failed")
            return buf.tobytes()

        return await asyncio.to_thread(callback)
