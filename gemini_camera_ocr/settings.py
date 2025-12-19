from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def __init__(self) -> None:
        super().__init__()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    log_level: str = "INFO"
    log_format: str = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    log_json: bool = False

    gemini_api_key: str
    gemini_model: str = "gemini-flash-latest"

    camera_index: int = 0
    interval_sec: float = 10.0
    jpeg_quality: int = 90

    # ===== Prompt =====
    ocr_prompt: str = (
        "あなたはOCRエンジンです。\n"
        "画像内の文字を日本語/英語ともに可能な限り正確に抽出してください。\n"
        "出力は次のJSONのみ:\n"
        '{"text": "...", "notes": "..."}\n'
        "- text: 読み取れた全文（改行は適切に維持）\n"
        "- notes: 読み取りが不確かな箇所や、判別不能だった箇所のメモ（なければ空文字）\n"
    )
