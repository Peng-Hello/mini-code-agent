# Project Context

## Purpose
mini-code-agent is the smallest building block of an AI coding system — a tiny yet functional CLI agent that demonstrates how an agent loop, memory, and tools work together. This project serves as a foundational example of how to build a code agent similar to Claude Code CLI agent app.

The project aims to provide a minimal but complete implementation of an AI-powered coding assistant that can:
- Execute agent loops to process user requests
- Maintain memory/context across interactions
- Utilize tools to perform coding tasks
- Provide an interactive CLI interface for users

## Tech Stack
- **Language**: Python 3.9+
- **UI Framework**: Textual - for building rich terminal user interfaces
- **AI Core**: DSPy - a framework for programming LLMs with code for complex tasks
- **CLI**: Click or Typer - for command-line interface structure
- **Configuration**: Pydantic - for type-safe configuration management

## Project Conventions

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all function signatures
- Use Pydantic models for data validation
- Maximum line length: 88 characters (Black formatting)
- Use f-strings for string formatting
- Use dataclasses for simple data containers

### Architecture Patterns
- **Agent Loop Pattern**: Implement a cyclical process of:
  1. Read user input
  2. Process with LLM using DSPy
  3. Execute actions/tools
  4. Update memory/state
  5. Render output via Textual UI
  6. Repeat

- **Modular Design**:
  - `core/` - Agent loop, memory management, and core logic
  - `tools/` - Reusable tools the agent can call
  - `ui/` - Textual interface components
  - `config/` - Configuration and settings management

- **Memory Management**: Separate short-term (conversation) and long-term (project context) memory

### Testing Strategy
- Unit tests for core logic (pytest)
- Integration tests for agent loop
- CLI tests for command-line interface
- Aim for >80% code coverage
- Test DSPy signatures independently
- Use golden files for UI output testing

### Git Workflow
- Main branch: `master`
- Feature branches: `feature/short-description`
- Commit messages follow conventional commits: `type(scope): description`
  - Types: feat, fix, docs, refactor, test, chore
- Pull requests required for all changes
- Squash and merge preferred

## Domain Context

### DSPy Framework
DSPy (Declarative Self-Improving Python) is the core AI framework used for:
- Defining LLM-powered signatures
- Composing complex pipelines
- Self-improving agent behaviors
- Structured output handling

Key concepts:
- **Signatures**: Define input/output schemas for LLM calls
- **Modules**: Composable building blocks for LLM pipelines
- **Optimizers**: Improve prompts automatically

### Textual Framework
Textual provides a modern TUI (Terminal User Interface) with:
- Rich widgets and layouts
- Event-driven architecture
- CSS-like styling for terminals
- Responsive design

### Agent Loop Components
1. **Input Handler**: Processes user commands
2. **Context Manager**: Maintains conversation and project memory
3. **Tool Executor**: Runs available tools
4. **LLM Interface**: Uses DSPy to reason and decide actions
5. **Output Renderer**: Displays results via Textual UI

## Important Constraints
- Must run in terminal environments (no GUI dependency)
- Should work on Linux, macOS, and Windows
- Minimal dependencies for easy installation
- Performance: Agent loop should respond within reasonable time
- Memory usage: Keep within reasonable limits for small systems

## External Dependencies

### Core Libraries
- **dspy-ai**: LLM framework for agent reasoning
- **textual**: Terminal UI framework
- **pydantic**: Data validation and settings management
- **typer** or **click**: CLI framework

### Optional Dependencies
- **rich**: Enhanced terminal formatting
- **anyio**: Async I/O utilities
- **loguru**: Advanced logging

### Environment Variables
- `OPENAI_API_KEY` or similar LLM API keys for DSPy
- `MINI_CODE_AGENT_CONFIG`: Optional path to config file

### Services
- LLM providers supported by DSPy (OpenAI, Anthropic, local models)
- Vector databases for long-term memory (optional, future enhancement)
