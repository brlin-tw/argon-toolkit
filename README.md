# Argon FastMCP Server (`argon-toolkit`)

A local FastMCP server that lets **Flash 3.8** act as the primary Antigravity orchestrator while calling **Gemini 4 Argon** (`gemini-4-argon`) via the Google GenAI API (billed against AI Studio / Google Developer Program credits).

## Workflow (`argon-review-loop`)

1. **Pre-process with Flash**: Scope relevant files and summarize project state into a compact `project_context` string so Argon doesn't waste tokens crawling the repository.
2. **Draft Plan (`argon_draft_plan`)**: Send the task and `project_context` to `gemini-4-argon` to produce a concrete implementation plan.
3. **Adversarial Review (`argon_adversarial_review`)**: Critique the proposed plan for bugs, edge cases, security flaws, and over-engineering.
4. **Revise Plan (`argon_revise_plan`)**: Have `gemini-4-argon` address valid critiques and produce the final plan.
5. **Direct Query (`query_argon`)**: Send ad-hoc reasoning or debugging tasks with configurable `thinking_level` (`LOW`, `MEDIUM`, `HIGH`).

Every response appends token usage (`input`, `output`, `thoughts`, `total`) so you can track against the 1M monthly free Argon output token quota.

## Configuration & Registration

Set your AI Studio API key (with a spend cap configured in Google Cloud / AI Studio) in the MCP server configuration:

- **Global Configuration**: `~/.gemini/config/mcp_config.json`
- **Project Configuration**: `.gemini/settings.json`

```json
{
  "mcpServers": {
    "argon-toolkit": {
      "command": "/home/brlin/文件/antigravity-cli-with-argon-fastmcp/.venv/bin/python3",
      "args": [
        "/home/brlin/文件/antigravity-cli-with-argon-fastmcp/server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "YOUR_AI_STUDIO_API_KEY"
      }
    }
  }
}
```

## Verification

Run the self-check suite:

```bash
.venv/bin/python3 test_argon_client.py
```

Inspect registered tools via the FastMCP CLI:

```bash
PATH="$(pwd)/.venv/bin:$PATH" .venv/bin/fastmcp list server.py
```
