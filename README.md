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

3. **get_workspace_info**: Returns information about a workspace folder
   - Parameters: `workspace_folder` (string, required) - Path to the workspace folder
   - Returns statistics about the files in the workspace, including:
     - Total number of files and directories
     - Total size of all files
     - Distribution of file types
     - Largest files
     - Newest files
   - In VS Code, you can use `${workspaceFolder}` as the parameter value

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

### Testing with VS Code

To use this MCP server with VS Code:

1. Install VS Code and the MCP extension for VS Code
2. Configure the MCP extension by adding the server configuration to your VS Code settings:
   - Open VS Code settings (File > Preferences > Settings or Ctrl+,)
   - Click on the "Open Settings (JSON)" icon in the top right corner
   - Add the configuration from `vscode_settings_example.json` to your settings file
   - Save the settings file and restart VS Code
3. Open a workspace in VS Code
4. Use the MCP extension to call the tools, particularly the `get_workspace_info` tool which can use the `${workspaceFolder}` variable

Example of using the `get_workspace_info` tool in VS Code:
- The tool will automatically receive the current workspace path when you use `${workspaceFolder}` as the parameter
- This allows you to analyze any workspace you have open in VS Code

Two sample VS Code configuration files are provided in this repository:
- `vscode_config_sample.json`: Contains just the MCP server configuration
- `vscode_settings_example.json`: A more comprehensive example showing how to integrate the MCP server configuration into your VS Code settings file

The key configuration is under the `mcp.servers` setting, which tells VS Code how to start and communicate with your MCP server.
