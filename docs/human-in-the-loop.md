# Human-in-the-Loop Review

Operational AI workflows should support people making better decisions, not silently replace judgment.

## Why Human Review Matters

This workflow turns messy operational inputs into structured briefings. That is useful, but the output can affect priorities, ownership, customer follow-up, and leadership reporting. A human reviewer helps ensure the briefing is accurate, fair, and operationally safe before it becomes part of the team's working record.

Human review is especially important for:

- action item ownership
- risk severity
- customer-sensitive context
- missing or ambiguous source details
- decisions that require business judgment

## Where Approval Happens Today

In the current prototype, `scripts/run_sample.py` generates structured JSON and can publish the briefing into the Notion Customer Briefs database. The Notion page is the practical review surface.

The current implementation does not include automated approval routing. The recommended status is `Draft` until an operations lead or account owner has checked the content. After review, the Notion entry can be manually approved, updated, or routed for follow-up.

## What Reviewers Should Verify

- The summary accurately reflects the source material.
- Stakeholders and owners are named correctly.
- Risks are specific and actionable.
- Next steps have clear owners and realistic dates.
- Open questions are captured instead of guessed.
- The customer or account name is correct.
- The risk level matches the actual operational concern.
- The briefing does not imply decisions that were not made.
- Sensitive or uncertain details are handled carefully.

## Future n8n Extension

n8n is planned for a future phase and is not implemented yet. It could later extend the human review loop by:

- triggering the workflow when a transcript or note is added
- sending review notifications to the right owner
- moving Notion status from `Draft` to `Ready for Review`
- routing high-risk briefings for extra approval
- logging approvals and rejections
- retrying failed Claude or Notion API calls

## Recommended Adoption Pattern

1. Run the workflow on a small set of low-risk inputs.
2. Have an operations lead approve each briefing before publishing.
3. Track common edits reviewers make.
4. Improve prompts and Notion fields based on repeated review patterns.
5. Only then expand automation through n8n.
