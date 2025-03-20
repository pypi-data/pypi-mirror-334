"""
Suada Python SDK

This package provides a Python interface to Suada's Business Analyst API.
"""

from .client import Suada
from .types import (
    ChatMessage,
    ChatPayload,
    SuadaConfig,
    SuadaResponse,
    ReasoningInfo,
    SupervisorState,
    WebSearchResult,
    IntegrationInfo,
    DataRetrieval,
    Analysis,
)

__version__ = "1.2.0-rc.1"
__all__ = [
    "Suada",
    "ChatMessage",
    "ChatPayload",
    "SuadaConfig",
    "SuadaResponse",
    "ReasoningInfo",
    "SupervisorState",
    "WebSearchResult",
    "IntegrationInfo",
    "DataRetrieval",
    "Analysis",
] 