"""
Azure DevOps MCP Server

A simple MCP server that exposes Azure DevOps capabilities.
"""
import argparse
from mcp.server.fastmcp import FastMCP
from mcp_azure_devops.resources import work_items

# Create a FastMCP server instance with a name
mcp = FastMCP("Azure DevOps")

# Register work item resources
work_items.register_resources(mcp)

def main():
    """Entry point for the command-line script."""
    parser = argparse.ArgumentParser(description="Run the Azure DevOps MCP server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to")
    # Add more command-line arguments as needed
    
    args = parser.parse_args()
    
    # Register all resources and tools
    # work_items.register_resources(mcp)
    # ... register other resources and tools
    
    # Start the server
    mcp.run()

if __name__ == "__main__":
    main()