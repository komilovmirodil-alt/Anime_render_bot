import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
VIDEO_CODES_FILE = DATA_DIR / "video_codes.json"
SERIALS_FILE = DATA_DIR / "serials.json"


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not VIDEO_CODES_FILE.exists():
        VIDEO_CODES_FILE.write_text("{}", encoding="utf-8")
    if not SERIALS_FILE.exists():
        SERIALS_FILE.write_text("{}", encoding="utf-8")


def _load_json_dict(path: Path) -> Dict[str, Any]:
    _ensure_storage()
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, OSError):
        return {}
    return {}


def _save_json_dict(path: Path, data: Dict[str, Any]) -> None:
    _ensure_storage()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_video_codes() -> Dict[str, str]:
    data = _load_json_dict(VIDEO_CODES_FILE)
    return {str(k): str(v) for k, v in data.items()}


def save_video_codes(data: Dict[str, str]) -> None:
    _save_json_dict(VIDEO_CODES_FILE, data)


def load_serials() -> Dict[str, Any]:
    data = _load_json_dict(SERIALS_FILE)
    cleaned: Dict[str, Any] = {}

    for code, raw_serial in data.items():
        if not isinstance(raw_serial, dict):
            continue

        title = str(raw_serial.get("title", "Serial"))
        photo_id = str(raw_serial.get("photo_id", ""))
        raw_parts = raw_serial.get("parts", {})

        parts: Dict[str, str] = {}
        if isinstance(raw_parts, dict):
            parts = {str(k): str(v) for k, v in raw_parts.items()}

        cleaned[str(code)] = {
            "title": title,
            "photo_id": photo_id,
            "parts": parts,
        }

    return cleaned


def save_serials(data: Dict[str, Any]) -> None:
    _save_json_dict(SERIALS_FILE, data)
