# Mini Code Agent Core

Core functionality for the mini-code-agent AI coding assistant.

## Overview

This package provides a modular, configurable AI coding agent built on top of DSPy (Declarative Self-Improving Python). It includes a collection of tools for file operations, web interactions, and an agent loop that can reason and execute tasks.

## Architecture

```
core/
├── agent.py              # Agent core logic (DSPy ReAct integration)
├── config.py             # Configuration management (YAML-based)
└── tool/                 # Tool modules (single import point)
    ├── __init__.py       # Unified export of all tools
    ├── file_tools.py     # File operations (read_file, list_file_tree)
    ├── search_tools.py   # Search tools (search_in_files)
    ├── path_tools.py     # Path management (create_path, edit_path)
    ├── edit_tools.py     # File editing (replace_in_file)
    ├── web_tools.py      # Web interactions (fetch_website_html, use_search_engine)
    └── io_tools.py       # I/O utilities (tell_human_something)
```

## Quick Start

### Basic Usage

```python
from core.agent import Agent

# Initialize agent with default config
agent = Agent()

# Or specify a custom config directory
agent = Agent(config_path="/path/to/project")

# Process a requirement
result = agent(requirement="Read the README.md file and summarize it")
print(result.solution)
```

### Using Tools Directly

All tools can be imported through a single import statement:

```python
from core.tool import (
    read_file,
    list_file_tree,
    search_in_files,
    create_path,
    edit_path,
    replace_in_file,
    fetch_website_html,
    use_search_engine,
    tell_human_something,
)

# Use tools directly
content = read_file("path/to/file.py")
tree = list_file_tree("path/to/directory")
create_path("path/to/dir", "new_file.py", is_file=True, content="# New file")
```

## Configuration

### Configuration Files

The agent supports configuration via YAML files in two locations (in order of priority):

1. **Project Path**: `<current directory>/.mini-code-agent/config.yaml`
2. **User Path**: `<home directory>/.mini-code-agent/config.yaml`

### Configuration Format

Create a `.mini-code-agent/config.yaml` file:

```yaml
# DSPy (LLM) Configuration
dspy:
  # Model identifier (e.g., "openai/gpt-4", "anthropic/claude-3", "openai/deepseek-chat")
  model: "openai/deepseek-chat"

  # API Key for your LLM provider
  api_key: "your-api-key-here"

  # Optional: API base URL (for custom endpoints or proxies)
  api_base: "https://api.deepseek.com/v1"

  # Allow async tool conversion (usually keep as true)
  allow_tool_async_sync_conversion: true

# Agent Configuration
agent:
  # Maximum iterations for ReAct agent (prevents infinite loops)
  max_iters: 200
```

### Default Configuration

If no config file is found, the agent uses these defaults:

- **Model**: `openai/deepseek-chat`
- **Max Iterations**: `200`
- **Async Conversion**: `enabled`

## Tools Reference

### File Tools

#### `read_file(file_path: str, encoding: str = "utf-8") -> str`
Read file contents and return as string.

**Parameters:**
- `file_path`: Path to the file to read
- `encoding`: File encoding (default: "utf-8")

**Returns:** File content as string, or empty string on error

**Example:**
```python
content = read_file("README.md")
print(content)
```

#### `list_file_tree(root_path: str, indent: str = "  ") -> str`
Generate a formatted directory tree.

**Parameters:**
- `root_path`: Root directory path
- `indent`: Indentation style (default: two spaces)

**Returns:** Directory tree as string

**Example:**
```python
tree = list_file_tree(".")
print(tree)
```

### Search Tools

#### `search_in_files(root_path: str, pattern: str, encoding: str = "utf-8", exclude_dirs: Set[str] = None) -> List[str]`
Search for regex pattern in files and return matching file paths.

**Parameters:**
- `root_path`: Search root directory
- `pattern`: Regular expression pattern
- `encoding`: File encoding (default: "utf-8")
- `exclude_dirs`: Directories to exclude (default: {".idea", "node_modules"})

**Returns:** List of matching file paths

**Example:**
```python
files = search_in_files(".", r"def\s+test")
for f in files:
    print(f)
```

### Path Tools

#### `create_path(base_path: str, name: str, is_file: bool = True, content: str = None) -> str`
Create a file or directory.

**Parameters:**
- `base_path`: Base directory path
- `name`: File or directory name
- `is_file`: Create file (True) or directory (False)
- `content`: Content to write if creating a file

**Returns:** Absolute path to created file/directory, or empty string on error

**Example:**
```python
path = create_path(".", "new_file.py", is_file=True, content="# New file")
print(f"Created: {path}")
```

#### `edit_path(path: str, new_name: str = None, new_content: str = None) -> str`
Edit a file or directory (rename or update content).

**Parameters:**
- `path`: Path to edit
- `new_name`: New name (optional)
- `new_content`: New content (files only, optional)

**Returns:** New path on success, None on error

**Example:**
```python
new_path = edit_path("old_name.py", new_name="new_name.py")
new_path = edit_path("file.py", new_content="New content")
```

### Edit Tools

#### `replace_in_file(file_path: str, pattern: str, replacement: str, encoding: str = "utf-8") -> bool`
Replace content in file using regex pattern.

**Parameters:**
- `file_path`: File path
- `pattern`: Regex pattern to match
- `replacement`: Replacement string
- `encoding`: File encoding (default: "utf-8")

**Returns:** True if replacement successful, False otherwise

**Example:**
```python
success = replace_in_file("file.py", r"old_text", r"new_text")
```

### Web Tools

#### `fetch_website_html(url: str, wait: int = 3) -> str`
Fetch rendered HTML from a website using Playwright.

**Parameters:**
- `url`: Target URL
- `wait`: Seconds to wait for JavaScript rendering (default: 3)

**Returns:** Rendered HTML content

**Example:**
```python
import asyncio
html = asyncio.run(fetch_website_html("https://example.com"))
```

#### `use_search_engine(question: str, engine: str = "bing") -> List[dict]`
Search using a search engine and parse results.

**Parameters:**
- `question`: Search query
- `engine`: Search engine (only "bing" supported)

**Returns:** List of results with title, url, and desc

**Example:**
```python
import asyncio
results = asyncio.run(use_search_engine("Python programming"))
for r in results:
    print(f"{r['title']}: {r['url']}")
```

### I/O Tools

#### `tell_human_something(message: str)`
Print a status message to the user.

**Parameters:**
- `message`: Message to display

**Example:**
```python
tell_human_something("I am now reading the file...")
```

## Development

### Adding New Tools

1. Create a new module in `core/tool/`
2. Implement your tool function with proper docstring and type hints
3. Export it in `core/tool/__init__.py`
4. Add it to the `__all__` list

Example:
```python
# core/tool/my_tools.py
def my_new_tool(param1: str, param2: int = 10) -> str:
    """Description of the tool."""
    # Implementation
    return "result"

# core/tool/__init__.py
from .my_tools import my_new_tool
# Add to __all__
```

### Testing Tools

Test your implementation:
```python
from core.tool import my_new_tool
result = my_new_tool("test", param2=20)
```

## License

This is part of the mini-code-agent project.
