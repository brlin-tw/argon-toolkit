import os
from typing import Literal
from fastmcp import FastMCP
from google import genai
from google.genai import types

mcp = FastMCP("ArgonToolkit")
DEFAULT_MODEL = os.environ.get("ARGON_MODEL", "gemini-4-argon")


def _get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Configure it in mcp_config.json 'env' or your shell environment."
        )
    return genai.Client(api_key=api_key)


@mcp.tool
async def query_argon(
    prompt: str,
    context: str = "",
    system_instruction: str = "You are an expert software architect and engineer.",
    thinking_level: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM",
    model: str = DEFAULT_MODEL,
) -> str:
    """Send a targeted prompt and pre-processed context package to Gemini 4 Argon."""
    client = _get_client()
    contents = f"## Context Package\n{context}\n\n## Task\n{prompt}" if context else prompt
    response = await client.aio.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel[thinking_level]
            ),
        ),
    )
    text = response.text or ""
    u = response.usage_metadata
    if u:
        return (
            f"{text}\n\n---\n"
            f"*Token Usage (`{model}`): input={u.prompt_token_count}, "
            f"output={u.candidates_token_count}, thoughts={u.thoughts_token_count}, "
            f"total={u.total_token_count}*"
        )
    return text


@mcp.tool
async def argon_draft_plan(
    task: str,
    project_context: str,
    thinking_level: Literal["LOW", "MEDIUM", "HIGH"] = "HIGH",
) -> str:
    """Draft an implementation plan with Gemini 4 Argon from Flash's pre-processed context package."""
    return await query_argon(
        prompt=task,
        context=project_context,
        system_instruction=(
            "You are the Lead Architect in an orchestrated planning loop. "
            "Analyze the pre-processed project context and draft a concrete, step-by-step "
            "implementation plan covering files to modify, edge cases, and verification steps."
        ),
        thinking_level=thinking_level,
    )


@mcp.tool
async def argon_adversarial_review(
    plan: str,
    project_context: str,
    review_model: str = DEFAULT_MODEL,
    thinking_level: Literal["LOW", "MEDIUM", "HIGH"] = "HIGH",
) -> str:
    """Perform an adversarial review of a proposed implementation plan."""
    return await query_argon(
        prompt=f"## Proposed Plan\n{plan}\n\nCritically review this plan.",
        context=project_context,
        system_instruction=(
            "You are an Adversarial Code & Architecture Reviewer. "
            "Critically evaluate the proposed plan against the project context. "
            "Identify unstated assumptions, bugs, edge cases, security issues, and over-engineering."
        ),
        thinking_level=thinking_level,
        model=review_model,
    )


@mcp.tool
async def argon_revise_plan(
    original_plan: str,
    review_feedback: str,
    project_context: str = "",
    thinking_level: Literal["LOW", "MEDIUM", "HIGH"] = "HIGH",
) -> str:
    """Revise an implementation plan with Gemini 4 Argon based on adversarial review feedback."""
    return await query_argon(
        prompt=(
            f"## Original Plan\n{original_plan}\n\n"
            f"## Adversarial Review Feedback\n{review_feedback}\n\n"
            "Produce the revised implementation plan."
        ),
        context=project_context,
        system_instruction=(
            "You are the Lead Architect revising an implementation plan after an adversarial review. "
            "Address all valid critiques, reject false positives with brief justification, and output "
            "the final actionable implementation plan."
        ),
        thinking_level=thinking_level,
    )


if __name__ == "__main__":
    mcp.run()
