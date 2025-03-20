from mcp.server.fastmcp import FastMCP
from typing import Dict, Any
import logging

"""Model Context Protocol server for the LegiDB class."""

# Configure logger
logger = logging.getLogger("legi_mcp")

print("Starting")

mcp = FastMCP(
    name="policyengine-mcp",
    instructions="Server providing access to PolicyEngine"
)

print("Got server")


@mcp.tool(description="Calculate income tax from employment income")
async def get_income_tax(employment_income: float) -> float:
    from policyengine_uk import Simulation

    sim = Simulation(
        situation={
            "employment_income": {"2025": employment_income}
        },
    )

    return sim.calculate("income_tax", 2025).values[0]

print("Got tool")

def start(port: int = None):
    """Start the MCP server."""

    try:
        if port is not None:
            mcp.settings.port = port
            logger.info(
                f"Server starting with SSE transport on port {mcp.settings.port}"
            )
            mcp.run(transport="sse")
        else:
            logger.info("Server starting with stdio transport")
            mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    start()