"""
Configuration management for mini-code-agent.
"""

import yaml
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class DSPyConfig(BaseModel):
    """DSPy configuration settings."""

    model: str = Field(description="LM model identifier")
    api_key: str = Field(description="API key")
    api_base: Optional[str] = Field(
        default=None, description="API base URL"
    )
    allow_tool_async_sync_conversion: bool = Field(
        default=True, description="Allow async tool conversion"
    )


class AgentConfig(BaseModel):
    """Agent configuration settings."""

    max_iters: int = Field(
        default=200, description="Maximum iterations for ReAct"
    )


class Config(BaseModel):
    """Main configuration class."""

    dspy: DSPyConfig
    agent: AgentConfig

    @classmethod
    def load(cls, config_dir: Optional[str] = None) -> "Config":
        """
        Load configuration from YAML file.

        Priority:
        1. Project path: <cwd>/.mini-code-agent/config.yaml
        2. User path: <home>/.mini-code-agent/config.yaml

        :param config_dir: Optional directory to check first
        :return: Config instance
        """
        config_paths = []

        # Project path (highest priority)
        if config_dir:
            project_path = (
                Path(config_dir) / ".mini-code-agent" / "config.yaml"
            )
            config_paths.append(project_path)
        else:
            cwd_path = Path.cwd() / ".mini-code-agent" / "config.yaml"
            config_paths.append(cwd_path)

        # User path (fallback)
        home_path = Path.home() / ".mini-code-agent" / "config.yaml"
        config_paths.append(home_path)

        # Try to load from any of the paths
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        config_data = yaml.safe_load(f)
                    return cls(**config_data)
                except Exception as e:
                    print(
                        f"Warning: Failed to load config from "
                        f"{config_path}: {e}"
                    )

        # No config found, use defaults
        print("Warning: No config file found, using default configuration")
        return cls._default()

    @classmethod
    def _default(cls) -> "Config":
        """Create default configuration."""
        return cls(
            dspy=DSPyConfig(
                model="openai/deepseek-chat",
                api_key="",
                allow_tool_async_sync_conversion=True,
            ),
            agent=AgentConfig(max_iters=200),
        )

    def save(self, config_dir: Optional[str] = None) -> str:
        """
        Save configuration to YAML file.

        :param config_dir: Directory to save config (defaults to user home)
        :return: Path to saved file
        """
        if config_dir:
            config_path = (
                Path(config_dir) / ".mini-code-agent" / "config.yaml"
            )
        else:
            config_path = Path.home() / ".mini-code-agent" / "config.yaml"

        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Save config
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(
                self.model_dump(),
                f,
                default_flow_style=False,
                allow_unicode=True,
            )

        return str(config_path)
