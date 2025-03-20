"""
ClickHouse MCP Server

A server for interacting with ClickHouse databases through MCP.
"""

from .server import mcp


def main() -> None:
    """Run the ClickHouse MCP server"""
    mcp.run()


__all__ = ['mcp', 'main']
