from mcp.server.fastmcp import FastMCP
import os
import pathlib
from typing import Dict, List, Any

# Initialize FastMCP server
mcp = FastMCP("python-ai-course-mcp-server")

@mcp.tool()
async def get_info() -> str:
    """Get information about this MCP server.
    
    Returns information about the purpose and capabilities of this demo MCP server.
    """
    return (
        "This is a demo MCP server created using the MCP SDK.\n\n"
        "It demonstrates how to create a simple MCP server with tools "
        "that can be used by MCP clients like Claude Desktop and VSCode."
    )

@mcp.tool()
async def get_greetings(name: str) -> str:
    """Get a personalized greeting.
    
    Args:
        name: The name of the person to greet
    
    Returns a friendly greeting that includes the provided name.
    """
    return f"Hello, {name}! This is a demo MCP server."

@mcp.tool()
async def get_workspace_info(workspace_folder: str) -> str:
    """Get information about a workspace folder.
    
    Args:
        workspace_folder: Path to the workspace folder (can use ${workspaceFolder} in VS Code)
    
    Returns information about the files in the workspace, including counts and statistics.
    """
    try:
        # Ensure the path exists
        if not os.path.exists(workspace_folder):
            return f"Error: The path '{workspace_folder}' does not exist."
        
        if not os.path.isdir(workspace_folder):
            return f"Error: '{workspace_folder}' is not a directory."
        
        # Initialize statistics
        stats = {
            "total_files": 0,
            "total_directories": 0,
            "file_types": {},
            "total_size_bytes": 0,
            "largest_files": [],
            "newest_files": []
        }
        
        # Keep track of files for sorting later
        all_files = []
        
        # Walk through the directory tree
        for root, dirs, files in os.walk(workspace_folder):
            # Skip hidden directories (starting with .)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            stats["total_directories"] += len(dirs)
            
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    file_mtime = os.path.getmtime(file_path)
                    
                    # Update statistics
                    stats["total_files"] += 1
                    stats["total_size_bytes"] += file_size
                    
                    # Track file extensions
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()
                    if ext:
                        stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                    else:
                        stats["file_types"]["no_extension"] = stats["file_types"].get("no_extension", 0) + 1
                    
                    # Add to all_files for sorting later
                    all_files.append({
                        "path": os.path.relpath(file_path, workspace_folder),
                        "size": file_size,
                        "mtime": file_mtime
                    })
                except (PermissionError, OSError):
                    # Skip files we can't access
                    continue
        
        # Get top 5 largest files
        largest_files = sorted(all_files, key=lambda x: x["size"], reverse=True)[:5]
        stats["largest_files"] = [
            f"{f['path']} ({format_size(f['size'])})" for f in largest_files
        ]
        
        # Get top 5 newest files
        newest_files = sorted(all_files, key=lambda x: x["mtime"], reverse=True)[:5]
        stats["newest_files"] = [
            f"{f['path']} ({format_timestamp(f['mtime'])})" for f in newest_files
        ]
        
        # Format the output
        result = f"Workspace: {workspace_folder}\n\n"
        result += f"Total Files: {stats['total_files']}\n"
        result += f"Total Directories: {stats['total_directories']}\n"
        result += f"Total Size: {format_size(stats['total_size_bytes'])}\n\n"
        
        result += "File Types:\n"
        for ext, count in sorted(stats["file_types"].items(), key=lambda x: x[1], reverse=True)[:10]:
            result += f"  {ext}: {count}\n"
        
        result += "\nLargest Files:\n"
        for file in stats["largest_files"]:
            result += f"  {file}\n"
        
        result += "\nNewest Files:\n"
        for file in stats["newest_files"]:
            result += f"  {file}\n"
        
        return result
    except Exception as e:
        return f"Error analyzing workspace: {str(e)}"


def format_size(size_bytes):
    """Format size in bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0 or unit == 'TB':
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def format_timestamp(timestamp):
    """Format a timestamp to a human-readable date."""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
