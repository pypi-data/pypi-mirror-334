"""Main entry point for the MCP Tree Explorer."""

import sys
from typing import Any, List, Optional, Union

from mcp.server.fastmcp import Context, FastMCP

from .tree_utils import install_tree, is_tree_installed, run_tree


def create_server() -> FastMCP:
    """Create the MCP server with tree tools."""
    # Create a simple MCP server focused on tools
    mcp = FastMCP("Project Tree Explorer")
    
    @mcp.tool()
    async def project_tree(
        directory: str = ".",
        depth: Optional[Any] = None,
        ignore: Optional[str] = None,
        keep: Optional[str] = None,
        ctx: Context = None,
    ) -> str:
        """
        Show the directory structure using the tree command.
        
        Args:
            directory: The directory to examine (default: current directory)
            depth: Maximum depth of the tree (unlimited if not specified or 0)
            ignore: Additional patterns to ignore, comma-separated
            keep: Patterns to keep even if they match auto-ignore patterns, comma-separated
        """
        # Handle depth validation (accept empty string, None, or convert to int)
        if depth == "" or depth is None:
            depth = None
        elif isinstance(depth, int):
            pass  # Keep as is
        else:
            try:
                depth = int(depth)
            except (ValueError, TypeError):
                return f"Error: depth parameter must be a valid integer or empty, got '{depth}'"
        
        # Check if tree is installed
        if not is_tree_installed():
            if ctx:
                ctx.info("Tree command not found. Attempting to install...")
            
            success, message = await install_tree()
            if not success:
                return message
            
            output = f"{message}\n\n"
        else:
            output = ""
        
        # Process the ignore and keep patterns
        ignore_patterns: List[str] = []
        if ignore:
            ignore_patterns = [p.strip() for p in ignore.split(",")]
        
        keep_patterns: List[str] = []
        if keep:
            keep_patterns = [p.strip() for p in keep.split(",")]
        
        # Show the tree command configuration
        output += f"Examining directory: {directory}\n"
        if depth is not None and depth > 0:
            output += f"Maximum depth: {depth}\n"
        else:
            output += "Maximum depth: unlimited\n"
            depth = None  # Set to None if 0 or negative to indicate unlimited depth
            
        if ignore_patterns:
            output += f"Additional ignore patterns: {', '.join(ignore_patterns)}\n"
        if keep_patterns:
            output += f"Keep patterns: {', '.join(keep_patterns)}\n"
        
        output += "\n"
        
        # Execute tree command
        if ctx:
            ctx.info(f"Running tree in {directory}...")
        
        tree_output = await run_tree(
            directory=directory,
            depth=depth,
            ignore_patterns=ignore_patterns,
            keep_patterns=keep_patterns,
        )
        
        return output + tree_output
    
    return mcp


def main() -> None:
    """Run the MCP Tree Explorer server with stdio transport."""
    try:
        server = create_server()
        server.run(transport="stdio")
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()