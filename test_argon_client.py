"""Self-check and example client for the ArgonToolkit FastMCP server."""
# Copyright 2026 林博仁(Buo-ren Lin) <buo.ren.lin@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from fastmcp import Client
import server


async def verify_server():
    server_path = Path(__file__).parent / "server.py"

    # 1. Verify FastMCP tool registration over stdio
    async with Client(server_path) as mcp_client:
        tools = await mcp_client.list_tools()
        tool_names = {t.name for t in tools}
        expected = {
            "query_argon",
            "argon_draft_plan",
            "argon_adversarial_review",
            "argon_revise_plan",
        }
        assert expected.issubset(tool_names), f"Missing tools: {expected - tool_names}"
        print(f"Verified {len(tools)} registered MCP tools: {sorted(tool_names)}")

    # 2. Verify Review Loop tool execution with mocked GenAI client
    mock_response = MagicMock()
    mock_response.text = "1. Edit server.py\n2. Run tests"
    mock_response.usage_metadata.prompt_token_count = 120
    mock_response.usage_metadata.candidates_token_count = 45
    mock_response.usage_metadata.thoughts_token_count = 80
    mock_response.usage_metadata.total_token_count = 245

    mock_client = MagicMock()
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    with patch.object(server, "_get_client", return_value=mock_client):
        draft = await server.argon_draft_plan(
            task="Add Argon MCP tools",
            project_context="server.py uses FastMCP",
        )
        assert "1. Edit server.py" in draft
        assert "Token Usage (`gemini-4-argon`): input=120, output=45" in draft

        review = await server.argon_adversarial_review(
            plan=draft,
            project_context="server.py uses FastMCP",
        )
        assert "Token Usage" in review

        revised = await server.argon_revise_plan(
            original_plan=draft,
            review_feedback=review,
            project_context="server.py uses FastMCP",
        )
        assert "Token Usage" in revised
        assert mock_client.aio.models.generate_content.call_count == 3
        print("Verified 3-step Review Loop (draft -> review -> revise) successfully.")


if __name__ == "__main__":
    asyncio.run(verify_server())
