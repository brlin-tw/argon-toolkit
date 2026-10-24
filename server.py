import sys
from fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("ArgonToolkit")

@mcp.tool()
def calculate_expression(expression: str) -> str:
    """Safely evaluate basic mathematical expressions.
    
    Args:
        expression: Mathematical expression string, e.g. '2 ** 10 + 42'.
    """
    # Safe eval for basic math
    allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
    code = compile(expression, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise ValueError(f"Use of '{name}' is not permitted.")
    result = eval(code, {"__builtins__": {}}, allowed_names)
    return str(result)

@mcp.tool()
def inspect_system_environment() -> dict[str, str]:
    """Inspect environment information relevant to agent execution."""
    return {
        "python_version": sys.version,
        "platform": sys.platform,
        "status": "ready",
        "target_model": "gemini-4-argon",
    }

@mcp.tool()
def echo_message(message: str) -> str:
    """Echo back a message with a confirmation prefix.
    
    Args:
        message: The message to echo.
    """
    return f"Argon Server received: {message}"

if __name__ == "__main__":
    mcp.run()
