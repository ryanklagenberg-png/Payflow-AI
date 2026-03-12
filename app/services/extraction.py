import base64
import asyncio
import json
import logging
from pathlib import Path

import anthropic

from app.config import settings
from app.prompts.invoice_extraction import INVOICE_EXTRACTION_PROMPT
from app.schemas.invoice import ExtractionResult

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]  # seconds between retries

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
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            message = client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=4096,
                system=[
                    {
                        "type": "text",
                        "text": INVOICE_EXTRACTION_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
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
                logger.error("Failed to parse Claude response (attempt %d): %s", attempt + 1, response_text[:500])
                last_error = ValueError("AI extraction returned invalid JSON")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAYS[attempt])
                continue

            return ExtractionResult(**data)

        except (anthropic.APITimeoutError, anthropic.APIConnectionError) as e:
            last_error = e
            logger.warning("Claude API connection error (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, e)
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAYS[attempt])

        except anthropic.RateLimitError as e:
            last_error = e
            logger.warning("Claude API rate limited (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, e)
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAYS[attempt] * 2)  # wait longer for rate limits

        except anthropic.APIStatusError as e:
            # Server errors (500, 529) are retryable; client errors (400, 401) are not
            if e.status_code >= 500:
                last_error = e
                logger.warning("Claude API server error %d (attempt %d/%d): %s", e.status_code, attempt + 1, MAX_RETRIES, e)
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAYS[attempt])
            else:
                raise

    raise last_error or ValueError("Extraction failed after all retries")
