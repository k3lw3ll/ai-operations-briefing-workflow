from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "extract_briefing.md"
INPUT_PATH = ROOT / "sample_inputs" / "customer_transcript.txt"
OUTPUT_PATH = ROOT / "sample_outputs" / "customer_briefing.json"


def main() -> None:
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    transcript = INPUT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{TRANSCRIPT_OR_NOTE}}", transcript)

    print("Prepared Claude prompt from sample transcript.")
    print(f"Prompt characters: {len(prompt)}")
    print(f"Sample output available at: {OUTPUT_PATH}")
    print()
    print("Next implementation step: send this prompt to Claude and store reviewed output in Notion.")


if __name__ == "__main__":
    main()
