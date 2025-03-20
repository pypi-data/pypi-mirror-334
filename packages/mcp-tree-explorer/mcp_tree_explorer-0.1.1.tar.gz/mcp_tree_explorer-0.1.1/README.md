# MCP Tree Explorer

A lightweight MCP tool for directory tree visualization in Cursor.

## Features

- Visualize directory structures with the `tree` command
- Smart filtering of common large directories (node_modules, .git, etc.)
- Customizable ignore and keep patterns
- Automatic installation of the `tree` command if not available
- Works on Windows, macOS, and Linux

## Installation

```bash
# Using pip
pip install mcp-tree-explorer

# Using uv
uv pip install mcp-tree-explorer
```

## Usage with Cursor

Configure Cursor to use this tool by editing your Cursor configuration file:

```json
{
  "tools": {
    "mcp-tree-explorer": {
      "command": "mcp-tree-explorer"
    }
  }
}
```

## Tool Parameters

The `project_tree` tool accepts these parameters:

- `directory`: The directory to examine (default: current directory)
- `depth`: Maximum depth of the tree (optional, unlimited if not specified)
- `ignore`: Additional patterns to ignore, comma-separated (optional)
- `keep`: Patterns to keep even if they match auto-ignore patterns, comma-separated (optional)

Example usage in Cursor:
- "Show me the directory structure of this project"
- "Run tree in the src directory but include node_modules"
- "Show me a tree of the project, ignoring test files but keeping the dist folder"

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-tree-explorer.git
cd mcp-tree-explorer

# Install in development mode
uv pip install -e .
```

## License

MIT