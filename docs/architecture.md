# Lightweight Architecture

This project starts with a small, inspectable workflow instead of a full application framework.

## Flow

1. Input arrives as a transcript, operational note, ticket, or weekly update.
2. A prompt template asks Claude to extract a structured briefing.
3. The generated JSON is reviewed by a human operator.
4. Approved output is stored in Notion.
5. n8n can later orchestrate scheduling, routing, approval, and retries.

## Components

- Claude API: structured analysis and briefing extraction.
- n8n: future orchestration layer for triggers and handoffs.
- Notion: destination for approved operational briefings.
- Human reviewer: validates risks, owners, next steps, and sensitive decisions.

## Design Principles

- Keep the workflow observable and easy to change.
- Treat AI output as a draft until reviewed.
- Preserve source context for auditability.
- Add automation only after the human process is understood.
