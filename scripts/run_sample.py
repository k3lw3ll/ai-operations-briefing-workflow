import json
import os
from datetime import date
from pathlib import Path

import requests
from anthropic import Anthropic
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "extract_briefing.md"
INPUT_PATH = ROOT / "sample_inputs" / "customer_transcript.txt"
OUTPUT_PATH = ROOT / "sample_outputs" / "customer_briefing_generated.json"
RAW_OUTPUT_PATH = ROOT / "sample_outputs" / "customer_briefing_raw.txt"
DEFAULT_MODEL = "claude-sonnet-4-5"
NOTION_VERSION = "2022-06-28"


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


def get_customer_name(briefing: dict) -> str:
    return (
        briefing.get("customer")
        or briefing.get("account")
        or briefing.get("customer_name")
        or briefing.get("account_name")
        or "Unknown Customer"
    )


def get_risk_level(briefing: dict) -> str:
    if briefing.get("risk_level"):
        return briefing["risk_level"]
    if briefing.get("risks"):
        return "Medium"
    return "Low"


def as_text(value) -> str:
    if value is None:
        return "None provided."
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, dict):
        return ", ".join(f"{key}: {as_text(item)}" for key, item in value.items())
    if isinstance(value, list):
        return "\n".join(f"- {as_text(item)}" for item in value) or "None provided."
    return str(value)


def paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text[:2000]},
                }
            ]
        },
    }


def heading(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text},
                }
            ]
        },
    }


def briefing_blocks(briefing: dict) -> list[dict]:
    sections = [
        ("Summary", briefing.get("summary")),
        ("Stakeholders", briefing.get("stakeholders")),
        ("Risks", briefing.get("risks")),
        ("Next Steps", briefing.get("next_steps")),
        ("Open Questions", briefing.get("open_questions")),
        ("Human Review Required", briefing.get("human_review_required")),
    ]

    blocks = []
    for title, content in sections:
        blocks.append(heading(title))
        blocks.append(paragraph(as_text(content)))
    return blocks


def write_to_notion(briefing: dict) -> None:
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_database_id = os.getenv("NOTION_DATABASE_ID")

    if not notion_api_key or not notion_database_id:
        print("Notion output skipped: NOTION_API_KEY or NOTION_DATABASE_ID is missing.")
        return

    customer_name = get_customer_name(briefing)
    payload = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "Customer": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": customer_name},
                    }
                ]
            },
            "Status": {"select": {"name": "Draft"}},
            "Risk Level": {"select": {"name": get_risk_level(briefing)}},
            "Last Updated": {"date": {"start": date.today().isoformat()}},
            "Summary": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": as_text(briefing.get("summary"))[:2000]},
                    }
                ]
            },
        },
        "children": briefing_blocks(briefing),
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    page_url = response.json().get("url", "Notion page created")
    print(f"Wrote briefing to Notion: {page_url}")


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
    write_to_notion(briefing)


if __name__ == "__main__":
    main()
