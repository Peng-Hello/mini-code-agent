# Configuration Guide

This document describes how to configure the mini-code-agent.

## Configuration Files

The agent reads configuration from YAML files in the following locations (in priority order):

1. **Project Path** (highest priority): `<current working directory>/.mini-code-agent/config.yaml`
2. **User Path** (fallback): `<home directory>/.mini-code-agent/config.yaml`

If neither file exists, the agent uses default configuration values.

## Full Configuration Reference

### Minimal Configuration

```yaml
dspy:
  model: "openai/deepseek-chat"
  api_key: "your-api-key-here"
```

### Complete Configuration

```yaml
# Mini Code Agent Configuration

# DSPy (LLM) Configuration
dspy:
  # Model identifier
  # Examples:
  #   - "openai/gpt-4"
  #   - "anthropic/claude-3"
  #   - "openai/deepseek-chat"
  #   - "azure/gpt-35-turbo"
  model: "openai/deepseek-chat"

  # API Key for your LLM provider
  # This can also be set via environment variable: OPENAI_API_KEY
  api_key: "your-api-key-here"

  # Optional: API base URL
  # Useful for:
  #   - Custom endpoints
  #   - API proxies
  #   - Azure OpenAI Service
  #   - Local LLM servers
  api_base: "https://api.deepseek.com/v1"

  # Allow async tool conversion
  # Keep as true unless you have specific requirements
  allow_tool_async_sync_conversion: true

# Agent Configuration
agent:
  # Maximum iterations for ReAct agent loop
  # Prevents infinite loops in complex tasks
  # Range: 1-1000 (recommended: 200)
  max_iters: 200
```

## Configuration Options

### dspy Section

#### `model` (required)
**Type:** String
**Description:** Model identifier for the LLM provider

**Supported Providers:**

**OpenAI:**
```yaml
model: "openai/gpt-4"
# or
model: "openai/gpt-3.5-turbo"
```

**Anthropic:**
```yaml
model: "anthropic/claude-3"
```

**DeepSeek:**
```yaml
model: "openai/deepseek-chat"
api_base: "https://api.deepseek.com/v1"
```

**Azure OpenAI:**
```yaml
model: "your-deployment-name"
api_base: "https://your-resource.openai.azure.com/"
```

**Local/Ollama:**
```yaml
model: "openai/llama2"
api_base: "http://localhost:11434/v1"
```

#### `api_key` (required)
**Type:** String
**Description:** API key for your LLM provider

You can also set this via environment variable instead of in the config file:
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`

**Example:**
```bash
export OPENAI_API_KEY="sk-..."
```

Then in config:
```yaml
dspy:
  model: "openai/gpt-4"
  api_key: ""  # Will use environment variable
```

#### `api_base` (optional)
**Type:** String
**Description:** Custom API base URL

Use this for:
- Custom deployments
- API proxies
- Azure OpenAI
- Local LLM servers

#### `allow_tool_async_sync_conversion` (optional)
**Type:** Boolean
**Default:** `true`
**Description:** Allow DSPy to automatically convert tools between async/sync modes

### agent Section

#### `max_iters` (optional)
**Type:** Integer
**Default:** `200`
**Range:** 1-1000
**Description:** Maximum number of iterations for the ReAct agent

The ReAct agent uses a thought-action-observation loop. This setting prevents infinite loops in complex tasks.

**Recommended Values:**
- Simple tasks: 50
- Medium tasks: 200
- Complex tasks: 500
- Safety limit: 1000

## Configuration Examples

### OpenAI Configuration

```yaml
dspy:
  model: "openai/gpt-4"
  api_key: "sk-your-openai-key-here"
agent:
  max_iters: 200
```

### Anthropic Configuration

```yaml
dspy:
  model: "anthropic/claude-3"
  api_key: "sk-ant-your-anthropic-key-here"
agent:
  max_iters: 200
```

### DeepSeek Configuration

```yaml
dspy:
  model: "openai/deepseek-chat"
  api_key: "sk-your-deepseek-key-here"
  api_base: "https://api.deepseek.com/v1"
agent:
  max_iters: 200
```

### Azure OpenAI Configuration

```yaml
dspy:
  model: "your-deployment-name"
  api_key: "your-azure-key"
  api_base: "https://your-resource.openai.azure.com/"
agent:
  max_iters: 200
```

### Local/Ollama Configuration

```yaml
dspy:
  model: "openai/llama2"
  api_key: "ollama"  # Any string for Ollama
  api_base: "http://localhost:11434/v1"
agent:
  max_iters: 200
```

## Configuration File Locations

### Project-Level Configuration

Place `config.yaml` in your project root with the `.mini-code-agent` folder:

```
my-project/
├── .mini-code-agent/
│   └── config.yaml
├── src/
└── ...
```

This configuration will be used when running the agent from this directory.

### User-Level Configuration

Place `config.yaml` in your home directory:

**Linux/macOS:**
```
~/.mini-code-agent/config.yaml
```

**Windows:**
```
C:\Users\YourName\.mini-code-agent\config.yaml
```

### Priority Example

If you have both:

```
Project: /workspace/my-project/.mini-code-agent/config.yaml
User:    /home/user/.mini-code-agent/config.yaml
```

The **project-level** configuration takes priority.

## Validation

The configuration is validated using Pydantic. Invalid configurations will raise errors on agent initialization.

Common validation errors:

1. **Missing required fields:**
   ```
   ValidationError: api_key is required
   ```

2. **Invalid model type:**
   ```
   ValidationError: model must be a string
   ```

3. **Invalid max_iters value:**
   ```
   ValidationError: max_iters must be between 1 and 1000
   ```

## Troubleshooting

### "No config file found, using default configuration"

**Cause:** No configuration file exists in either location

**Solution:** Create a configuration file as described above

### "Failed to load config from ...: ..."

**Cause:** YAML syntax error in config file

**Solution:** Check your YAML syntax with an online validator

### "api_key is required"

**Cause:** API key not provided in config or environment

**Solution:** Add `api_key` to your config or set the environment variable

### Model not found errors

**Cause:** Invalid model identifier or API key

**Solution:**
1. Verify model name is correct
2. Check API key is valid
3. Ensure you have access to the model

## Security Best Practices

1. **Don't commit API keys to version control**
   - Add `.mini-code-agent/config.yaml` to `.gitignore`
   - Use environment variables for production

2. **Use environment variables for sensitive data:**
   ```yaml
   dspy:
     model: "openai/gpt-4"
     api_key: ""  # Use $OPENAI_API_KEY
   ```

3. **Use project-level config for development**
   - Use `.gitignore` to exclude it
   - Provide a `.mini-code-agent-config-template.yaml` template

4. **Use user-level config for personal use**
   - More secure than project-level
   - Shared across all projects

## Support

For issues with configuration, please check:
1. DSPy documentation: https://dspy-docs.vercel.app/
2. Your LLM provider's documentation
3. This project's issue tracker
