import asyncio
import logging

from .camera import Camera
from .gemini_ocr import GeminiOcr
from .logger import LoggingSettings, setup_logging
from .settings import Settings

logger = logging.getLogger(__name__)


def output_debug_frame(frame: bytes) -> None:
    with open("debug.jpg", "wb") as f:
        f.write(frame)


async def run_loop() -> None:
    settings = Settings()

    setup_logging(
        LoggingSettings(
            level=settings.log_level,
            format=settings.log_format,
            json=settings.log_json,
        )
    )

    async with Camera.open(index=settings.camera_index) as camera:
        logger.info(f"Camera initialized (index={settings.camera_index})")

        gemini = GeminiOcr(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            prompt=settings.ocr_prompt,
        )

        while True:
            try:
                frame = await camera.read_frame(jpeg_quality=settings.jpeg_quality)
                gemini_response = await gemini.ocr_image(frame)
                await asyncio.to_thread(output_debug_frame, frame)
                gemini_response = await gemini.ocr_image(frame)
                logger.info(
                    "\n".join(
                        [
                            "-" * 40,
                            gemini_response.text,
                            gemini_response.notes or "None",
                            "-" * 40,
                        ]
                    )
                )
            except Exception as e:
                logger.error("Error during processing", exc_info=e)
            finally:
                await asyncio.sleep(settings.interval_sec)


def main() -> None:
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.info("App terminated by user")
