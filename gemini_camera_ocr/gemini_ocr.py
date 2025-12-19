from typing import Optional

from google import genai
from google.genai import types
from pydantic import BaseModel


class GeminiOcrResponse(BaseModel):
    text: str
    notes: Optional[str] = None


class GeminiOcr:
    def __init__(self, api_key: str, model: str, prompt: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.prompt = prompt

    async def ocr_image(self, jpeg_bytes: bytes) -> GeminiOcrResponse:
        image_part = types.Part.from_bytes(data=jpeg_bytes, mime_type="image/jpeg")

        resp = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[self.prompt, image_part],
        )
        if resp.text is None:
            raise RuntimeError("Gemini OCR response text is None.")

        text = resp.text.strip("```json").rstrip("```").strip()

        return GeminiOcrResponse.model_validate_json(text)
