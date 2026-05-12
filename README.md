# AI Operations Briefing Workflow

## Project Overview

AI Operations Briefing Workflow is a prototype operational AI workflow system for turning customer transcripts or internal operations notes into structured, reviewable briefings.

The current implementation demonstrates a working flow from sample transcript to Claude API analysis, structured JSON generation, and optional Notion database publishing. It is intentionally lightweight and focuses on workflow design, operational adoption, and human-in-the-loop review rather than chatbot interaction.

This project is a prototype operational workflow system intended for experimentation and portfolio demonstration purposes.

## Problem / Use Case

Operations teams often receive important updates through scattered formats: call transcripts, account notes, tickets, documents, spreadsheets, and meeting summaries. Turning those inputs into consistent leadership briefings can be slow, manual, and error-prone.

This prototype explores how AI can help standardize that process by extracting:

- concise summaries
- stakeholders
- operational risks
- next steps
- open questions
- human review requirements

The goal is not to replace operators. The goal is to create a repeatable workflow where AI drafts structured operational intelligence and a human reviewer validates the result before it becomes part of the system of record.

## Goals

- Demonstrate operational AI workflow orchestration
- Use the Claude API for structured analysis
- Support future n8n orchestration
- Store outputs in Notion
- Emphasize workflow design, operational adoption, and human-in-the-loop systems

## Current Workflow

```text
sample transcript
  -> Claude API
  -> structured JSON
  -> Notion Customer Briefs database
  -> human review
```

The working sample flow is implemented in `scripts/run_sample.py`.

1. Read `sample_inputs/customer_transcript.txt`.
2. Load `prompts/extract_briefing.md`.
3. Send the transcript and prompt to Claude.
4. Parse and write structured JSON to `sample_outputs/customer_briefing_generated.json`.
5. If Notion credentials are present, create a new Notion database entry.
6. Keep the generated briefing available for human review.

## Current Features

- Claude API integration using the Anthropic Python SDK
- Local `.env` configuration with no hardcoded secrets
- Structured JSON extraction prompt
- Robust response cleanup for JSON parsing
- Local generated JSON output
- Optional Notion database publishing
- Human-in-the-loop workflow documentation
- Lightweight project structure without unnecessary frameworks

## Project Structure

- `sample_inputs/` contains example source material for analysis.
- `sample_outputs/` contains example structured outputs.
- `prompts/` contains prompt templates for Claude.
- `scripts/` contains lightweight automation scripts.
- `docs/` contains workflow and adoption notes.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add the required API keys.

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Run the sample workflow:

```bash
python scripts/run_sample.py
```

## Environment Variables

Required for Claude analysis:

```text
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-5
```

Optional for Notion output:

```text
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

If the Notion variables are missing, the script still writes the local generated JSON file and skips Notion publishing.

## Example Output

The generated JSON follows this shape:

```json
{
  "customer": "Northstar Logistics",
  "summary": "Northstar Logistics wants to reduce the time spent consolidating regional weekly updates into leadership briefings.",
  "stakeholders": [],
  "risks": [],
  "next_steps": [],
  "open_questions": [],
  "human_review_required": true
}
```

A fuller sample is available in `sample_outputs/customer_briefing.json`.

## Planned Roadmap

- Add richer sample inputs for multiple operational scenarios
- Add optional validation for generated JSON fields
- Add clearer risk-level classification rules
- Add n8n workflow orchestration for scheduled runs and approvals
- Add Notion screenshots and demo assets
- Add retry and error-handling notes for production-like operations

## Portfolio / Demo Positioning

This repository demonstrates an operational AI workflow prototype, not a chatbot. It is designed to show how AI can fit into business operations by transforming messy source material into structured, reviewable outputs.

Useful demo talking points:

- AI workflow orchestration across Claude and Notion
- structured extraction from unstructured operational inputs
- human approval before publishing
- lightweight architecture that can later be orchestrated with n8n
- practical adoption pattern for operations, customer success, and leadership reporting

## Design Note

This scaffold intentionally avoids LangChain, vector databases, frontend UI, and a full n8n implementation for now. The workflow should stay easy to inspect while the operational process is still being refined.
```

This scaffold intentionally avoids unnecessary frameworks so the workflow design can evolve before the implementation becomes heavy.
