"""Utilities for working with the tree command."""

import platform
import shutil
import subprocess
from typing import List, Optional, Tuple


# Default patterns to ignore
DEFAULT_IGNORE_PATTERNS = [
    "node_modules",
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    ".env",
    ".next",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "coverage",
    "target",
    "bin",
    "obj",
    "*.pyc",
    "*.log",
]


def get_system() -> str:
    """Get the current operating system."""
    return platform.system().lower()


def is_tree_installed() -> bool:
    """Check if the tree command is installed."""
    return shutil.which("tree") is not None


async def install_tree() -> Tuple[bool, str]:
    """
    Attempt to install the tree command.
    
    Returns:
        Tuple[bool, str]: Success status and installation message
    """
    system = get_system()
    message = "The 'tree' command is not installed. "
    
    try:
        if system == "darwin":  # macOS
            message += "Attempting to install using Homebrew...\n"
            subprocess.run(["brew", "install", "tree"], check=True, capture_output=True)
        elif system == "linux":
            distro = ""
            try:
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if line.startswith("ID="):
                            distro = line.split("=")[1].strip().strip('"')
                            break
            except:
                pass
            
            if distro in ["ubuntu", "debian"]:
                message += "Attempting to install using apt...\n"
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "tree"], check=True, capture_output=True)
            elif distro in ["fedora", "centos", "rhel"]:
                message += "Attempting to install using yum...\n"
                subprocess.run(["sudo", "yum", "install", "-y", "tree"], check=True, capture_output=True)
            else:
                return False, f"{message}Couldn't determine Linux distribution for automatic installation. Please install it manually."
        elif system == "windows":
            # Try scoop first, then chocolatey
            try:
                message += "Attempting to install using Scoop...\n"
                subprocess.run(["scoop", "install", "tree"], check=True, capture_output=True)
            except:
                try:
                    message += "Attempting to install using Chocolatey...\n"
                    subprocess.run(["choco", "install", "tree", "-y"], check=True, capture_output=True)
                except:
                    return False, f"{message}Automatic installation failed. Please install it manually."
        else:
            return False, f"{message}Automatic installation is not supported on {system}. Please install it manually."
        
        # Check if installation succeeded
        if not is_tree_installed():
            return False, f"{message}Installation attempted but 'tree' command is still not available. Please install it manually."
        
        return True, f"{message}Successfully installed 'tree'!"
    except Exception as e:
        return False, f"{message}Failed to install 'tree': {str(e)}. Please install it manually."


async def run_tree(
    directory: str = ".",
    depth: Optional[int] = None,
    ignore_patterns: List[str] = None,
    keep_patterns: List[str] = None,
) -> str:
    """
    Run the tree command with specified options.
    
    Args:
        directory: Directory to run tree in
        depth: Maximum depth of the tree (None for unlimited)
        ignore_patterns: Patterns to ignore
        keep_patterns: Patterns to keep (overrides ignore patterns)
        
    Returns:
        str: Output of the tree command
    """
    system = get_system()
    
    # Combine default ignore patterns with user-provided ones
    if ignore_patterns is None:
        ignore_patterns = []
        
    all_ignore_patterns = DEFAULT_IGNORE_PATTERNS + ignore_patterns
    
    # Remove patterns that should be kept
    if keep_patterns:
        all_ignore_patterns = [p for p in all_ignore_patterns if p not in keep_patterns]
    
    if system in ["darwin", "linux"]:
        # Unix-like systems
        cmd = ["tree"]
        
        # Add depth limit if specified
        if depth is not None:
            cmd.extend(["-L", str(depth)])
        
        # Join patterns with pipe for tree's -I parameter
        if all_ignore_patterns:
            patterns_str = "|".join(all_ignore_patterns)
            cmd.extend(["-I", patterns_str])
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=directory, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Error running tree command: {e.stderr}\n"
            
            # Try fallback without ignore patterns
            try:
                result = subprocess.run(
                    ["tree"], 
                    cwd=directory,
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                output += "Fallback tree output (without filters):\n"
                output += result.stdout
            except Exception as nested_e:
                output += f"Fallback also failed: {str(nested_e)}. Please check your tree installation."
            
            return output
    
    elif system == "windows":
        # Windows has a very limited tree command
        cmd = ["tree", "/A", "/F"]
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=directory,
                capture_output=True, 
                text=True, 
                check=True
            )
            output = result.stdout
            output += "\nNote: Windows tree command doesn't support filtering out directories."
            return output
        except subprocess.CalledProcessError as e:
            return f"Error running tree command: {str(e)}"
    
    else:
        return f"Unsupported operating system: {system}"