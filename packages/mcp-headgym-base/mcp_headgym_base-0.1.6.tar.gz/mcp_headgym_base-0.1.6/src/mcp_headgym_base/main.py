"""
FastMCP Screenshot Example

Give Claude a tool to capture and view screenshots.
"""

import io

from mcp.server.fastmcp import FastMCP


# Create server
mcp = FastMCP("HeadGym")



@mcp.tool()
async def list_experts() -> str:
    """Lists all experts in the HeadGym directory

    """
    return "Expert 1: @murat Dr. John Doe\nExpert 2: @nikola Dr. Jane Doe"

@mcp.tool()
async def use_expert(expert_slug: str, query: str) -> str:
    """Uses an expert to handle the query

    """
    return f"Expert {expert_slug} is handling the query: {query}"


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
