import asyncio
import logging

from tqdm.asyncio import tqdm

from .camera import Camera
from .gemini_ocr import GeminiOcr
from .logger import LoggingSettings, setup_logging
from .settings import Settings

logger = logging.getLogger(__name__)


def format(text: str) -> str:
    return "\n".join(
        [
            "-" * 40,
            text,
            "-" * 40,
        ]
    )


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
            history_max_turns=settings.history_max_turns,
        )

        async def ocr_image() -> None:
            for _ in tqdm(range(10), desc="Countdown", bar_format="{bar}"):
                await asyncio.sleep(3 / 10)

            frame = await camera.read_frame(jpeg_quality=settings.jpeg_quality)
            if settings.output_debug_image:
                with open("debug_image.jpg", "wb") as f:
                    f.write(frame)
            gemini_response = await gemini.ocr_image(frame)
            logger.info(format(gemini_response))

        while True:
            try:
                await ocr_image()
            except Exception as e:
                logger.error("Error during processing", exc_info=e)
            finally:
                await asyncio.sleep(settings.interval_sec)


def main() -> None:
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.info("App terminated by user")
