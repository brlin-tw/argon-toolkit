"""Example integration: Invoking Gemini 4 Argon with the ArgonToolkit FastMCP server."""

import asyncio
from pathlib import Path
from fastmcp import Client
from google import genai


async def run_argon_agent():
    server_path = Path(__file__).parent / "server.py"

    # Connect to the FastMCP server
    mcp_client = Client(server_path)

    # Initialize Gemini client
    gemini_client = genai.Client()

    async with mcp_client:
        tools = await mcp_client.list_tools()
        print(f"Loaded {len(tools)} tools from FastMCP server:")
        for tool in tools:
            print(f" - {tool.name}: {tool.description}")

        # When GEMINI_API_KEY is configured in the environment, you can query gemini-4-argon:
        # response = await gemini_client.aio.models.generate_content(
        #     model="gemini-4-argon",
        #     contents="Inspect the system environment and compute 2 ** 16 using available tools.",
        # )
        # print("Gemini 4 Argon response:\n", response.text)


if __name__ == "__main__":
    asyncio.run(run_argon_agent())
