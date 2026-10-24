---
name: looping-with-argon
description: >-
  Orchestrate complex architectural planning and code reviews by delegating to
  Gemini 4 Argon (`gemini-4-argon`) via the `argon-toolkit` MCP server. Use when
  planning multi-file changes, designing complex features, or running an
  adversarial review loop while preserving Argon token quota.
---

# The looping-with-argon agent Skill

Use this workflow when acting as the orchestrator (e.g. Flash 3.8) to leverage `gemini-4-argon` via the local `argon-toolkit` FastMCP server without wasting Argon tokens crawling the entire codebase.

## Workflow Steps

### 1. Pre-process Context (Local Orchestrator)

Before calling any `argon-toolkit` MCP tool, scope the workspace yourself:
- Identify the relevant files using search/read tools.
- Summarize the current project state, constraints, and key code snippets into a compact `project_context` string.
- Never pass irrelevant files or raw directory dumps to Argon.

### 2. Draft Plan (`argon_draft_plan`)

Call `argon_draft_plan` on the `argon-toolkit` MCP server:
- `task`: Clear statement of the feature, bugfix, or architectural goal.
- `project_context`: The targeted context package assembled in Step 1.
- `thinking_level`: `"HIGH"` (default) for complex design, `"MEDIUM"` for standard changes.

### 3. Adversarial Review

Critically evaluate the drafted plan for edge cases, security flaws, race conditions, and over-engineering:
- **Option A (Zero Argon Quota)**: Perform the adversarial review directly as the orchestrator or delegate to a lightweight subagent.
- **Option B (Argon / Custom Reviewer)**: Call `argon_adversarial_review` with `plan` and `project_context` (optionally passing a lower-cost `review_model` or keeping `gemini-4-argon` when paired with an external frontier planner).

### 4. Revise Plan (`argon_revise_plan`)

If the adversarial review surfaces actionable critiques:
- Call `argon_revise_plan` with `original_plan`, `review_feedback`, and `project_context`.
- Present the final revised plan and token usage footer to the user for human-in-the-loop approval before executing code changes.
