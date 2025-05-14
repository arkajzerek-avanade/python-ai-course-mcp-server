from mcp.server.fastmcp import FastMCP
import os
import git
from typing import Dict, List, Any
from mcp.server import Server


# Initialize FastMCP server
mcp = FastMCP("python-ai-course-mcp-server")

server = Server("python-ai-course-mcp-server")


@mcp.tool()
async def get_info() -> str:
    """Get information about this MCP server.
    
    Returns information about the purpose and capabilities of this demo MCP server.
    """
    await server.request_context.session.send_log_message(
      level="info",
      data="get_info started successfully",
    )

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
    await server.request_context.session.send_log_message(
      level="info",
      data=f"get_greetings {name} started successfully",
    )

    return f"Hello, {name}! This is a demo MCP server."

@mcp.tool()
async def get_workspace_info(workspace_folder: str) -> str:
    """Get information about a workspace folder.
    
    Args:
        workspace_folder: Path to the workspace folder (can use ${workspaceFolder} in VS Code)
    
    Returns information about the files in the workspace, including counts and statistics.
    """

    await server.request_context.session.send_log_message(
      level="info",
      data=f"get_workspace_info {workspace_folder} started successfully",
    )

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


@mcp.tool()
async def get_repo_info(repo_path: str) -> str:
    """Get basic information about a Git repository status.
    
    Args:
        repo_path: Path to the Git repository (can use ${workspaceFolder} in VS Code)
    
    Returns basic Git repository status information.
    """
    
    await server.request_context.session.send_log_message(
      level="info",
      data=f"get_repo_info {repo_path} started successfully",
    )
    
    try:
        # Ensure the path exists
        if not os.path.exists(repo_path):
            return f"Error: The path '{repo_path}' does not exist."
        
        # Open the repository using GitPython
        try:
            repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            return f"Error: '{repo_path}' is not a Git repository."
        
        # Get basic repository information
        result = []
        
        # Repository path
        result.append(f"Repository: {repo_path}")
        
        # Current branch
        try:
            active_branch = repo.active_branch.name
            result.append(f"Current branch: {active_branch}")
        except TypeError:
            # This happens when in detached HEAD state
            result.append("Current branch: DETACHED HEAD")
        
        # Check if working directory is clean
        if repo.is_dirty():
            result.append("Status: Working directory has uncommitted changes")
        else:
            result.append("Status: Working directory is clean")
        
        # Count untracked files
        untracked_files = repo.untracked_files
        if untracked_files:
            result.append(f"Untracked files: {len(untracked_files)}")
        
        # Count modified files
        modified_files = [item.a_path for item in repo.index.diff(None)]
        if modified_files:
            result.append(f"Modified files: {len(modified_files)}")
        
        # Count staged files
        staged_files = [item.a_path for item in repo.index.diff('HEAD')]
        if staged_files:
            result.append(f"Staged files: {len(staged_files)}")
        
        # Get remote information if available
        if repo.remotes:
            result.append(f"Remote: {repo.remotes[0].name} ({repo.remotes[0].url})")
        
        return "\n".join(result)
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
