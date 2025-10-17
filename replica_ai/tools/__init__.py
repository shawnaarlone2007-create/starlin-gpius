from typing import Dict, List


def list_tools() -> List[Dict[str, str]]:
    return [
        {
            "name": "filesystem.read_file",
            "description": "Read a text file within the workspace",
        },
        {
            "name": "filesystem.write_file",
            "description": "Write a text file within the workspace",
        },
        {
            "name": "shell.run",
            "description": "Run a shell command with timeout",
        },
        {
            "name": "search.grep",
            "description": "Search for a pattern across files (scoped)",
        },
    ]
