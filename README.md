# Argon FastMCP Server (`argon-toolkit`)

A local FastMCP server that lets **Flash 3.8** act as the primary Antigravity orchestrator while calling **Gemini 4 Argon** (`gemini-4-argon`) via the Google GenAI API (billed against AI Studio / Google Developer Program credits).

<https://gitlab.com/brlin/argon-toolkit>  
[![The GitLab CI pipeline status badge of the project's `main` branch](https://gitlab.com/brlin/argon-toolkit/badges/main/pipeline.svg?ignore_skipped=true "Click here to check out the comprehensive status of the GitLab CI pipelines")](https://gitlab.com/brlin/argon-toolkit/-/pipelines) [![GitHub Actions workflow status badge](https://github.com/brlin-tw/argon-toolkit/actions/workflows/check-potential-problems.yml/badge.svg "GitHub Actions workflow status")](https://github.com/brlin-tw/argon-toolkit/actions/workflows/check-potential-problems.yml) [![pre-commit enabled badge](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white "This project uses pre-commit to check potential problems")](https://pre-commit.com/) [![REUSE Specification compliance badge](https://api.reuse.software/badge/gitlab.com/brlin/argon-toolkit "This project complies to the REUSE specification to decrease software licensing costs")](https://api.reuse.software/info/gitlab.com/brlin/argon-toolkit)

## Inspiration

Quoting [Qorsair's reply](https://www.reddit.com/r/google_antigravity/comments/1xd4lbk/comment/19rip6gx2ddcz/) in [Justice for the free pro users! : r/google_antigravity](https://www.reddit.com/r/google_antigravity/comments/1xd4lbk/justice_for_the_free_pro_users/):

> Trial plans lock Argon out of the Antigravity dropdown, but you still get free monthly GDP credits that unlock it via the API.
>
> And you should be using Flash 3.8 as the orchestrator anyway even if you had Argon if you care about quota, so the functionality is the same as a full Pro subscription.
>
> You just use Flash as the driver and have it call Argon through a local MCP server that bills against those credits.
>
> - Go to AI Studio, set up billing on a project, link the account with your GDP credits from your free pro plan
> - Paste a prompt into Flash telling it to build and register a FastMCP server targeting `gemini-4-argon`
> - Set a spend cap on the API key so you don’t blow past the free credits.
>
> You’re not locked out you just need to start using Flash + MCP the way Antigravity is designed to work.

and [this one](https://www.reddit.com/r/google_antigravity/comments/1xd4lbk/comment/19rjaeqsp53og/) as well:

> Setting this up is definitely worth it to claim your 1 million free Argon output tokens per month, which roll over for up to a year before switching to pay-as-you-go.
>
> To maximize these credits, I use an optimized workflow:
>
>- Pre-process with Flash: Use Flash to scope the relevant files and summarize the project state. Sending this targeted package prevents Argon from wasting tokens crawling the entire codebase.
>- The Review Loop: Argon drafts the plan, a lower cost model provides an adversarial review, and Argon handles the revisions.
>- Cost per Loop: This full cycle usually runs $0.15–$1.00 in credits, depending on complexity and your MCP configuration.
>
> If your needs are relatively light, the free credits will easily cover this. However, for heavy, continuous planning multiple times a day, you should get a $20 monthly subscription to a frontier model and plug that into Antigravity with MCP just like Argon. Then you can use Argon for the adversarial review portion of the loop.
>
> I use a cycle like this with Gemini and a frontier model and never have a problem with quota.

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
      "command": "/path/to/argon-toolkit/.venv/bin/python3",
      "args": [
        "/path/to/argon-toolkit/server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "YOUR_AI_STUDIO_API_KEY"
      }
    }
  }
}
```

Replace the `/path/to/argon-toolkit` placeholder text with the actual path to your Argon Toolkit project directory.

## Verification

Run the self-check suite:

```bash
.venv/bin/python3 test_argon_client.py
```

Inspect registered tools via the FastMCP CLI:

```bash
PATH="$(pwd)/.venv/bin:$PATH" .venv/bin/fastmcp list server.py
```

## Licensing

Unless otherwise noted([comment headers](https://reuse.software/spec-3.3/#comment-headers)/[REUSE.toml](https://reuse.software/spec-3.3/#reusetoml)), this product is licensed under [the 3.0 version of the GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html), or any of its more recent versions of your preference.

This work complies to [the REUSE Specification](https://reuse.software/spec/), refer to the [REUSE - Make licensing easy for everyone](https://reuse.software/) website for info regarding the licensing of this product.
