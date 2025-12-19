from google import genai
from google.genai import types


class GeminiHistory:
    def __init__(self, max_turns: int) -> None:
        self.max_turns = max_turns
        self.turns: list[str] = []

    def add_turn(self, response: str) -> None:
        self.turns.append(response)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    def get_history_content(self) -> list[types.ModelContent]:
        return [
            types.ModelContent(parts=[types.Part.from_text(text=turn)])
            for turn in self.turns
        ]


class GeminiOcr:
    def __init__(
        self, api_key: str, model: str, prompt: str, history_max_turns: int
    ) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.prompt = prompt
        self.history = GeminiHistory(max_turns=history_max_turns)

    async def ocr_image(self, jpeg_bytes: bytes) -> str:
        user = types.UserContent(
            parts=[types.Part.from_bytes(data=jpeg_bytes, mime_type="image/jpeg")],
        )
        resp = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[*self.history.get_history_content(), user],
            config=types.GenerateContentConfig(
                system_instruction=self.prompt,
            ),
        )
        if resp.text is None:
            raise RuntimeError("Gemini OCR response text is None.")

        self.history.add_turn(resp.text)
        return resp.text
