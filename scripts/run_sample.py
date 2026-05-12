import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "extract_briefing.md"
INPUT_PATH = ROOT / "sample_inputs" / "customer_transcript.txt"
OUTPUT_PATH = ROOT / "sample_outputs" / "customer_briefing_generated.json"
RAW_OUTPUT_PATH = ROOT / "sample_outputs" / "customer_briefing_raw.txt"
DEFAULT_MODEL = "claude-sonnet-4-5"


def clean_json_response(response_text: str) -> str:
    text = response_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
        text = text[first_brace : last_brace + 1]

    return text


def main() -> None:
    load_dotenv(ROOT / ".env")

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY is missing. Add it to a local .env file.")

    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    transcript = INPUT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{TRANSCRIPT_OR_NOTE}}", transcript)

    client = Anthropic()
    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL),
        max_tokens=2000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    response_text = response.content[0].text
    print("Raw Claude response:")
    print(response_text)
    print()

    cleaned_response = clean_json_response(response_text)
    try:
        briefing = json.loads(cleaned_response)
    except json.JSONDecodeError as error:
        RAW_OUTPUT_PATH.write_text(response_text, encoding="utf-8")
        raise RuntimeError(
            "Claude response could not be parsed as JSON. "
            f"Raw response saved to {RAW_OUTPUT_PATH}. "
            f"Parser error: {error}"
        ) from error

    OUTPUT_PATH.write_text(
        json.dumps(briefing, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote structured briefing JSON to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
