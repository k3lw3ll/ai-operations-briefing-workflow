# AI Operations Briefing Workflow

This project explores operational AI workflows using Claude, n8n, and Notion. It is a lightweight scaffold for turning customer or internal operations inputs into structured briefings that can be reviewed by humans and stored in operational systems.

## Goals

- Demonstrate operational AI workflow orchestration
- Use the Claude API for structured analysis
- Support future n8n orchestration
- Store outputs in Notion
- Emphasize workflow design, operational adoption, and human-in-the-loop systems

## Project Structure

- `sample_inputs/` contains example source material for analysis.
- `sample_outputs/` contains example structured outputs.
- `prompts/` contains prompt templates for Claude.
- `scripts/` contains lightweight automation scripts.
- `docs/` contains workflow and adoption notes.

## Intended Workflow

1. Collect a transcript, note, ticket, or operational update.
2. Send the input to Claude with a structured extraction prompt.
3. Review the generated briefing with a human operator.
4. Store the approved output in Notion.
5. Optionally orchestrate the flow through n8n.

## Setup

Copy `.env.example` to `.env` and add the required API keys.

```bash
pip install -r requirements.txt
```

This scaffold intentionally avoids unnecessary frameworks so the workflow design can evolve before the implementation becomes heavy.
