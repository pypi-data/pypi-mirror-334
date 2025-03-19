"""CUA (Computer Use) Agent for AI-driven computer interaction."""

__version__ = "0.1.0"

# Initialize telemetry when the package is imported
try:
    from core.telemetry import enable_telemetry, set_dimension

    # Enable telemetry by default
    enable_telemetry()
    # Set the package version as a dimension
    set_dimension("agent_version", __version__)
except ImportError:
    # Core telemetry not available
    pass

from .core.factory import AgentFactory
from .core.agent import ComputerAgent
from .providers.omni.types import LLMProvider, LLM
from .types.base import Provider, AgentLoop

__all__ = ["AgentFactory", "Provider", "ComputerAgent", "AgentLoop", "LLMProvider", "LLM"]
