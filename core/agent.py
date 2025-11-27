"""
Agent core implementation for mini-code-agent.
"""

import dspy
from typing import Optional
from .config import Config
from .tool import (
    read_file,
    list_file_tree,
    search_in_files,
    create_path,
    edit_path,
    replace_in_file,
    tell_human_something,
    fetch_website_html,
    use_search_engine,
)


class CodeAgentSignature(dspy.Signature):
    """Signature for the Code Agent."""

    requirement: str = dspy.InputField(desc="用户需求")
    solution: str = dspy.OutputField(desc="具体解决方案")


class Agent:
    """
    Main Agent class that integrates DSPy ReAct with tools and configuration.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Agent.

        :param config_path: Optional directory path to check for
            config.yaml first
        """
        self.config = Config.load(config_path)
        self._setup_dspy()
        self._setup_agent()

    def _setup_dspy(self):
        """Configure DSPy with loaded configuration."""
        lm = dspy.LM(
            self.config.dspy.model,
            api_key=self.config.dspy.api_key,
            api_base=self.config.dspy.api_base,
        )
        dspy.configure(
            lm=lm,
            allow_tool_async_sync_conversion=self.config.dspy
            .allow_tool_async_sync_conversion,
        )

    def _setup_agent(self):
        """Setup the ReAct agent with tools."""
        self.react_agent = dspy.ReAct(
            signature=CodeAgentSignature,
            tools=[
                read_file,
                list_file_tree,
                search_in_files,
                create_path,
                edit_path,
                replace_in_file,
                tell_human_something,
                fetch_website_html,
                use_search_engine,
            ],
            max_iters=self.config.agent.max_iters,
        )

    def __call__(self, requirement: str):
        """
        Process a user requirement.

        :param requirement: User's requirement or task description
        :return: Result from the agent
        """
        return self.react_agent(requirement=requirement)

    def run(self, requirement: str):
        """
        Alias for __call__ method.

        :param requirement: User's requirement or task description
        :return: Result from the agent
        """
        return self(requirement=requirement)


# Create default agent instance (backwards compatibility)
default_agent = Agent()
