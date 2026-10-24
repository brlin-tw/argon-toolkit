# Argon FastMCP Server

A FastMCP server built and registered to interface with **Gemini 4 Argon** (`gemini-4-argon`).

## Features

- **`calculate_expression`**: Safe arithmetic evaluation tool.
- **`inspect_system_environment`**: Runtime environment inspection for model execution status.
- **`echo_message`**: Echo validation utility for communication tests.

## Running the Server

Run directly with Python:
```bash
.venv/bin/python3 server.py
```

Inspect with FastMCP CLI:
```bash
PATH="$(pwd)/.venv/bin:$PATH" .venv/bin/fastmcp inspect server.py
PATH="$(pwd)/.venv/bin:$PATH" .venv/bin/fastmcp list server.py
```

Test calling a tool:
```bash
PATH="$(pwd)/.venv/bin:$PATH" .venv/bin/fastmcp call server.py echo_message message="Hello Argon"
```

## Registration

The server has been registered under:
- **Global Antigravity / Gemini Configuration**: `~/.gemini/config/mcp_config.json`
- **Project Configuration**: `.gemini/settings.json`
