#!/usr/bin/env python3
"""
Basic usage example for mini-code-agent.

This example demonstrates:
1. Initializing the agent
2. Using tools directly
3. Processing requirements with the agent
"""

import asyncio
from pathlib import Path

# Single import for all tools
from core.tool import (
    read_file,
    list_file_tree,
    search_in_files,
    create_path,
    edit_path,
    replace_in_file,
    tell_human_something,
)

from core.agent import Agent


def example_1_direct_tool_usage():
    """Example 1: Using tools directly"""
    print("\n=== Example 1: Direct Tool Usage ===\n")

    # Read a file
    print("Reading a file...")
    content = read_file(__file__)
    print(f"File length: {len(content)} characters")

    # List directory tree
    print("\nListing directory tree...")
    tree = list_file_tree(".")
    print("Directory contents (first 200 chars):")
    print(tree[:200] + "...")

    # Search for files
    print("\nSearching for Python files...")
    files = search_in_files(".", r"def\s+\w+")
    print(f"Found {len(files)} files with function definitions")

    # Create a new file
    print("\nCreating a new file...")
    new_file = create_path(
        ".",
        "example_output.txt",
        is_file=True,
        content="This is an example file created by mini-code-agent.\n"
    )
    print(f"Created: {new_file}")

    # Edit the file
    print("\nEditing the file...")
    edit_path(new_file, new_content="Updated content!\n")

    # Clean up
    Path(new_file).unlink()
    print("Cleaned up example file")


async def example_2_agent_usage():
    """Example 2: Using the Agent to process requirements"""
    print("\n=== Example 2: Agent Usage ===\n")

    # Initialize agent (will use default config or config.yaml)
    print("Initializing agent...")
    agent = Agent()

    # The agent needs API key to work, so this is just for demonstration
    print("Agent initialized (note: API key required for actual processing)")
    print(f"Agent config: {agent.config.dspy.model}")

    # Example of how to use the agent
    # Note: This requires valid API credentials to work
    print("\nTo use the agent with a real requirement:")
    print("  result = agent('Read the README.md file and summarize it')")
    print("  print(result.solution)")


def example_3_web_tools():
    """Example 3: Web tools (requires valid setup)"""
    print("\n=== Example 3: Web Tools ===\n")

    print("Note: Web tools require additional setup and valid API access")
    print("\nExample usage:")

    print("\n1. Fetch website HTML:")
    print("   html = await fetch_website_html('https://example.com')")
    print("   print(html[:200])")

    print("\n2. Search with Bing:")
    print("   results = await use_search_engine('Python programming')")
    print("   for r in results:")
    print("       print(f'{r[\"title\"]}: {r[\"url\"]}')")

    print("\nThese tools require:")
    print("  - Playwright installation: pip install playwright")
    print("  - Browser installation: python -m playwright install")
    print("  - Valid API credentials in config.yaml")


def example_4_configuration():
    """Example 4: Configuration management"""
    print("\n=== Example 4: Configuration ===\n")

    from core.config import Config

    print("Loading configuration...")
    config = Config.load()

    print(f"Model: {config.dspy.model}")
    print(f"Max iterations: {config.agent.max_iters}")

    print("\nTo create a config file:")
    print("  config.save('/path/to/.mini-code-agent')")
    print("  # Creates: /path/to/.mini-code-agent/config.yaml")

    print("\nConfig file locations (priority order):")
    print("  1. <current dir>/.mini-code-agent/config.yaml")
    print("  2. <home dir>/.mini-code-agent/config.yaml")


def example_5_advanced_usage():
    """Example 5: Advanced usage patterns"""
    print("\n=== Example 5: Advanced Usage ===\n")

    # Pattern 1: Using tools in a chain
    print("Pattern 1: Tool chaining")
    print("1. Search for files")
    print("2. Read matching files")
    print("3. Process content")
    print("4. Create output file")

    # Pattern 2: Custom workflow
    print("\nPattern 2: Custom workflow")
    workflow_steps = [
        ("Analyze project structure", "list_file_tree"),
        ("Find Python files", "search_in_files"),
        ("Check for TODO comments", "search_in_files"),
        ("Generate report", "create_path"),
    ]

    for description, tool in workflow_steps:
        print(f"  - {description}: {tool}")


def main():
    """Run all examples"""
    print("=" * 60)
    print("Mini Code Agent - Usage Examples")
    print("=" * 60)

    try:
        example_1_direct_tool_usage()
        example_2_agent_usage()
        example_3_web_tools()
        example_4_configuration()
        example_5_advanced_usage()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
