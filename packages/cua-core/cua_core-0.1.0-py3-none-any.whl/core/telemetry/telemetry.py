"""Universal telemetry module for collecting anonymous usage data.

This module provides a unified interface for telemetry collection,
using PostHog as the backend.
"""

from __future__ import annotations

import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Import telemetry backend
try:
    from core.telemetry.posthog_client import (
        PostHogTelemetryClient,
        get_posthog_telemetry_client,
    )

    POSTHOG_AVAILABLE = True
except ImportError:
    logger = logging.getLogger("cua.telemetry")
    logger.info("PostHog not available. Install with: pdm add posthog")
    POSTHOG_AVAILABLE = False

logger = logging.getLogger("cua.telemetry")


class TelemetryBackend(str, Enum):
    """Available telemetry backend types."""

    POSTHOG = "posthog"
    NONE = "none"


class UniversalTelemetryClient:
    """Universal telemetry client that delegates to the PostHog backend."""

    def __init__(
        self,
        project_root: Optional[Path] = None,
        backend: Optional[str] = None,
    ):
        """Initialize the universal telemetry client.

        Args:
            project_root: Root directory of the project
            backend: Backend to use ("posthog" or "none")
                     If not specified, will try PostHog
        """
        self.project_root = project_root

        # Determine which backend to use
        if backend and backend.lower() == "none":
            self.backend_type = TelemetryBackend.NONE
        else:
            # Auto-detect based on environment variables and available backends
            if POSTHOG_AVAILABLE:
                self.backend_type = TelemetryBackend.POSTHOG
            else:
                self.backend_type = TelemetryBackend.NONE
                logger.warning("PostHog is not available, telemetry will be disabled")

        # Initialize the appropriate client
        self._client = self._initialize_client()

    def _initialize_client(self) -> Any:
        """Initialize the appropriate telemetry client based on the selected backend."""
        if self.backend_type == TelemetryBackend.POSTHOG and POSTHOG_AVAILABLE:
            logger.debug("Initializing PostHog telemetry client")
            return get_posthog_telemetry_client(self.project_root)
        else:
            logger.debug("No telemetry client initialized")
            return None

    def increment(self, counter_name: str, value: int = 1) -> None:
        """Increment a named counter.

        Args:
            counter_name: Name of the counter
            value: Amount to increment by (default: 1)
        """
        if self._client:
            self._client.increment(counter_name, value)

    def record_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Record an event with optional properties.

        Args:
            event_name: Name of the event
            properties: Event properties (must not contain sensitive data)
        """
        if self._client:
            self._client.record_event(event_name, properties)

    def flush(self) -> bool:
        """Flush any pending events to the backend.

        Returns:
            bool: True if successful, False otherwise
        """
        if self._client:
            return self._client.flush()
        return False

    def enable(self) -> None:
        """Enable telemetry collection."""
        if self._client:
            self._client.enable()

    def disable(self) -> None:
        """Disable telemetry collection."""
        if self._client:
            self._client.disable()


# Global telemetry client instance
_universal_client: Optional[UniversalTelemetryClient] = None


def get_telemetry_client(
    project_root: Optional[Path] = None,
    backend: Optional[str] = None,
) -> UniversalTelemetryClient:
    """Get or initialize the global telemetry client.

    Args:
        project_root: Root directory of the project
        backend: Backend to use ("posthog" or "none")

    Returns:
        The global telemetry client instance
    """
    global _universal_client

    if _universal_client is None:
        _universal_client = UniversalTelemetryClient(project_root, backend)

    return _universal_client


def increment(counter_name: str, value: int = 1) -> None:
    """Increment a named counter using the global telemetry client.

    Args:
        counter_name: Name of the counter
        value: Amount to increment by (default: 1)
    """
    client = get_telemetry_client()
    client.increment(counter_name, value)


def record_event(event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
    """Record an event with optional properties using the global telemetry client.

    Args:
        event_name: Name of the event
        properties: Event properties (must not contain sensitive data)
    """
    client = get_telemetry_client()
    client.record_event(event_name, properties)


def flush() -> bool:
    """Flush any pending events using the global telemetry client.

    Returns:
        bool: True if successful, False otherwise
    """
    client = get_telemetry_client()
    return client.flush()


def enable_telemetry() -> None:
    """Enable telemetry collection globally."""
    client = get_telemetry_client()
    client.enable()


def disable_telemetry() -> None:
    """Disable telemetry collection globally."""
    client = get_telemetry_client()
    client.disable()
