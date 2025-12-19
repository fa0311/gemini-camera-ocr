# Gemini Camera OCR

OCR from camera using Gemini API at regular intervals.

## Installation

```bash
git clone https://github.com/fa0311/gemini-camera-ocr.git
cd gemini-camera-ocr
pip install -e .
```

## Configuration

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### Optional Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_MODEL` | `gemini-flash-latest` | Gemini model to use |
| `CAMERA_INDEX` | `0` | Camera device index |
| `INTERVAL_SEC` | `10.0` | Interval between OCR operations |
| `JPEG_QUALITY` | `90` | Image quality (0-100) |
| `HISTORY_MAX_TURNS` | `1` | Chat history length |
| `OCR_PROMPT` | (Japanese default) | Custom OCR prompt |
| `LOG_LEVEL` | `INFO` | Logging level |
| `OUTPUT_DEBUG_IMAGE` | `false` | Save debug image |

## Usage

```bash
python -m gemini_camera_ocr
```

The application will:

1. Capture images from your camera every N seconds
2. Extract text using Gemini API
3. Display the results in the console

Press `Ctrl+C` to stop.

## Requirements

- Python 3.10+
- Webcam or virtual camera
- Gemini API key
