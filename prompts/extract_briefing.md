# Operational Briefing Extraction Prompt

You are analyzing an operational customer transcript or internal workflow note.

Extract the information into structured JSON with the following fields:

- `summary`: A concise operational summary.
- `stakeholders`: People, teams, or roles involved, including their interests or responsibilities.
- `risks`: Operational, adoption, data quality, or execution risks.
- `next_steps`: Clear actions, owners, and due dates when available.
- `open_questions`: Questions that need follow-up or human clarification.
- `human_review_required`: Always set to `true` for this workflow.

Guidelines:

- Prefer concrete details from the source text.
- Do not invent owners, dates, or decisions.
- If information is missing, use `null` or add an item to `open_questions`.
- Keep the output suitable for review before posting to Notion.
- Return only valid JSON.

Input:

```text
{{TRANSCRIPT_OR_NOTE}}
```
