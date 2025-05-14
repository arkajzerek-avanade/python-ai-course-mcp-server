# Python AI Course MCP Server

A demo MCP (Model Context Protocol) server for Python AI course. This server demonstrates how to create a simple MCP server with tools that can be used by MCP clients like Claude Desktop and VSCode.

## Requirements

- Python 3.13 or higher

## Installation

This project uses [UV](https://github.com/astral-sh/uv) for package management. UV is a fast, reliable Python package installer and resolver.

### Installing UV

If you don't have UV installed, you can install it following the instructions on the [official UV documentation](https://github.com/astral-sh/uv#installation).

### Setting up the project

```bash
# Clone the repository
git clone [repository-url]
cd python-ai-course-mcp-server

# Create a virtual environment and install dependencies using UV
uv venv
uv pip install -e .
```

## Usage

```bash
# Activate the virtual environment (if not already activated)
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate

# Run the application
# Option 1: Using Python directly
python main.py

# Option 2: Using UV run (recommended)
uv run main.py
```

Using `uv run` is recommended as it provides a more streamlined experience when working with UV-managed projects.

## Development

To install development dependencies:

```bash
uv pip install -e ".[dev]"
```

## MCP Server Implementation

This project implements a simple MCP (Model Context Protocol) server with the following tools:

1. **get_info**: Returns information about the MCP server
   - No parameters required
   - Returns a text description of the server

2. **get_greetings**: Returns a personalized greeting
   - Parameters: `name` (string, required)
   - Returns a greeting message that includes the provided name

### How It Works

The server is built using the MCP SDK and follows the standard MCP protocol:

1. The server defines the available tools with their input schemas
2. When a client calls a tool, the server processes the request and returns the result
3. The server runs on stdio, making it compatible with MCP clients like Claude Desktop and VSCode

### Testing with Claude Desktop

To test this MCP server with Claude Desktop:

1. Install Claude Desktop from [claude.ai/download](https://claude.ai/download)
2. Configure Claude Desktop to use this server:
   - Locate your Claude Desktop configuration file at `%AppData%\Claude\claude_desktop_config.json` (on Windows)
   - If the file doesn't exist, create it
   - Use the sample configuration provided in `claude_desktop_config_sample.json` (adjust paths as needed)
   - Save the file and restart Claude Desktop
3. Claude will automatically start the server when needed
4. Ask Claude to use the `get_info` or `get_greetings` tools

Example of asking Claude to use the tools:
- "Can you use the get_info tool to tell me about this MCP server?"
- "Please use the get_greetings tool with my name 'John'."

A sample configuration file is provided in this repository as `claude_desktop_config_sample.json`. You may need to adjust the paths to match your system.
