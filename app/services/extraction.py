import base64
import json
import logging
from pathlib import Path

import anthropic

from app.config import settings
from app.prompts.invoice_extraction import INVOICE_EXTRACTION_PROMPT
from app.schemas.invoice import ExtractionResult

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

MIME_MAP = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".tiff": "image/tiff",
}


def _build_content_block(file_path: str) -> dict:
    ext = Path(file_path).suffix.lower()
    mime_type = MIME_MAP.get(ext)
    if not mime_type:
        raise ValueError(f"Unsupported file type: {ext}")

    file_bytes = Path(file_path).read_bytes()
    encoded = base64.standard_b64encode(file_bytes).decode("utf-8")

    if ext == ".pdf":
        return {
            "type": "document",
            "source": {"type": "base64", "media_type": mime_type, "data": encoded},
        }
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": mime_type, "data": encoded},
    }


async def extract_invoice(file_path: str) -> ExtractionResult:
    content_block = _build_content_block(file_path)

    message = client.messages.create(
        model=settings.CLAUDE_MODEL,
        max_tokens=4096,
        system=INVOICE_EXTRACTION_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    content_block,
                    {"type": "text", "text": "Extract all invoice data from this document."},
                ],
            }
        ],
    )

    response_text = message.content[0].text

    # Strip markdown code fences if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        lines = lines[1:]  # remove opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # remove closing fence
        response_text = "\n".join(lines)

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        logger.error("Failed to parse Claude response: %s", response_text[:500])
        raise ValueError("AI extraction returned invalid JSON")

    return ExtractionResult(**data)
