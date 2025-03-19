"""Telemetry client using PostHog for collecting anonymous usage data."""

from __future__ import annotations

import json
import logging
import os
import random
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import posthog
from core import __version__

logger = logging.getLogger("cua.telemetry")

# Controls how frequently telemetry will be sent (percentage)
TELEMETRY_SAMPLE_RATE = 5  # 5% sampling rate

# Public PostHog config for anonymous telemetry
# These values are intentionally public and meant for anonymous telemetry only
# https://posthog.com/docs/product-analytics/troubleshooting#is-it-ok-for-my-api-key-to-be-exposed-and-public
PUBLIC_POSTHOG_API_KEY = "phc_eSkLnbLxsnYFaXksif1ksbrNzYlJShr35miFLDppF14"
PUBLIC_POSTHOG_HOST = "https://eu.i.posthog.com"


@dataclass
class TelemetryConfig:
    """Configuration for telemetry collection."""

    enabled: bool = True  # Default to enabled (opt-out)
    sample_rate: float = TELEMETRY_SAMPLE_RATE
    project_root: Optional[Path] = None

    @classmethod
    def from_env(cls, project_root: Optional[Path] = None) -> TelemetryConfig:
        """Load config from environment variables."""
        # CUA_TELEMETRY=off to disable telemetry (opt-out)
        return cls(
            enabled=os.environ.get("CUA_TELEMETRY", "").lower() != "off",
            sample_rate=float(os.environ.get("CUA_TELEMETRY_SAMPLE_RATE", TELEMETRY_SAMPLE_RATE)),
            project_root=project_root,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "enabled": self.enabled,
            "sample_rate": self.sample_rate,
        }


def get_posthog_config() -> dict:
    """Get PostHog configuration for anonymous telemetry.

    Uses the public API key that's specifically intended for anonymous telemetry collection.
    No private keys are used or required from users.

    Returns:
        Dict with PostHog configuration
    """
    # Return the public config
    logger.debug("Using public PostHog configuration")
    return {"api_key": PUBLIC_POSTHOG_API_KEY, "host": PUBLIC_POSTHOG_HOST}


class PostHogTelemetryClient:
    """Collects and reports telemetry data via PostHog."""

    def __init__(
        self, project_root: Optional[Path] = None, config: Optional[TelemetryConfig] = None
    ):
        """Initialize PostHog telemetry client.

        Args:
            project_root: Root directory of the project
            config: Telemetry configuration, or None to load from environment
        """
        self.config = config or TelemetryConfig.from_env(project_root)
        self.installation_id = self._get_or_create_installation_id()
        self.initialized = False
        self.queued_events: List[Dict[str, Any]] = []
        self.start_time = time.time()

        # Log telemetry status on startup
        if self.config.enabled:
            logger.info(f"Telemetry enabled (sampling at {self.config.sample_rate}%)")
            # Initialize PostHog client if config is available
            self._initialize_posthog()
        else:
            logger.info("Telemetry disabled")

        # Create .cua directory if it doesn't exist and config is provided
        if self.config.project_root:
            self._setup_local_storage()

    def _initialize_posthog(self) -> bool:
        """Initialize the PostHog client with configuration.

        Returns:
            bool: True if initialized successfully, False otherwise
        """
        if self.initialized:
            return True

        posthog_config = get_posthog_config()

        try:
            # Initialize the PostHog client
            posthog.api_key = posthog_config["api_key"]
            posthog.host = posthog_config["host"]

            # Configure the client
            posthog.debug = os.environ.get("CUA_TELEMETRY_DEBUG", "").lower() == "on"
            posthog.disabled = not self.config.enabled

            # Identify this installation
            self._identify()

            # Process any queued events
            for event in self.queued_events:
                posthog.capture(
                    distinct_id=self.installation_id,
                    event=event["event"],
                    properties=event["properties"],
                )
            self.queued_events = []

            self.initialized = True
            return True
        except Exception as e:
            logger.debug(f"Failed to initialize PostHog: {e}")
            return False

    def _identify(self) -> None:
        """Identify the current installation with PostHog."""
        try:
            posthog.identify(
                distinct_id=self.installation_id,
                properties={
                    "version": __version__,
                    "is_ci": "CI" in os.environ,
                },
            )
        except Exception as e:
            logger.debug(f"Failed to identify with PostHog: {e}")

    def _get_or_create_installation_id(self) -> str:
        """Get or create a random installation ID.

        This ID is not tied to any personal information.
        """
        if self.config.project_root:
            id_file = self.config.project_root / ".cua" / "installation_id"
            if id_file.exists():
                try:
                    return id_file.read_text().strip()
                except Exception:
                    pass

            # Create new ID if not exists
            new_id = str(uuid.uuid4())
            try:
                id_file.parent.mkdir(parents=True, exist_ok=True)
                id_file.write_text(new_id)
                return new_id
            except Exception:
                pass

        # Fallback to in-memory ID if file operations fail
        return str(uuid.uuid4())

    def _setup_local_storage(self) -> None:
        """Create local storage directories and files."""
        if not self.config.project_root:
            return

        cua_dir = self.config.project_root / ".cua"
        cua_dir.mkdir(parents=True, exist_ok=True)

        # Store telemetry config
        config_path = cua_dir / "telemetry_config.json"
        with open(config_path, "w") as f:
            json.dump(self.config.to_dict(), f)

    def increment(self, counter_name: str, value: int = 1) -> None:
        """Increment a named counter.

        Args:
            counter_name: Name of the counter
            value: Amount to increment by (default: 1)
        """
        if not self.config.enabled:
            return

        # Apply sampling to reduce number of events
        if random.random() * 100 > self.config.sample_rate:
            return

        properties = {
            "value": value,
            "counter_name": counter_name,
            "version": __version__,
        }

        if self.initialized:
            try:
                posthog.capture(
                    distinct_id=self.installation_id,
                    event="counter_increment",
                    properties=properties,
                )
            except Exception as e:
                logger.debug(f"Failed to send counter event to PostHog: {e}")
        else:
            # Queue the event for later
            self.queued_events.append({"event": "counter_increment", "properties": properties})
            # Try to initialize now if not already
            self._initialize_posthog()

    def record_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Record an event with optional properties.

        Args:
            event_name: Name of the event
            properties: Event properties (must not contain sensitive data)
        """
        if not self.config.enabled:
            return

        # Apply sampling to reduce number of events
        if random.random() * 100 > self.config.sample_rate:
            return

        event_properties = {"version": __version__, **(properties or {})}

        if self.initialized:
            try:
                posthog.capture(
                    distinct_id=self.installation_id, event=event_name, properties=event_properties
                )
            except Exception as e:
                logger.debug(f"Failed to send event to PostHog: {e}")
        else:
            # Queue the event for later
            self.queued_events.append({"event": event_name, "properties": event_properties})
            # Try to initialize now if not already
            self._initialize_posthog()

    def flush(self) -> bool:
        """Flush any pending events to PostHog.

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.config.enabled:
            return False

        if not self.initialized and not self._initialize_posthog():
            return False

        try:
            posthog.flush()
            return True
        except Exception as e:
            logger.debug(f"Failed to flush PostHog events: {e}")
            return False

    def enable(self) -> None:
        """Enable telemetry collection."""
        self.config.enabled = True
        if posthog:
            posthog.disabled = False
        logger.info("Telemetry enabled")
        if self.config.project_root:
            self._setup_local_storage()
        self._initialize_posthog()

    def disable(self) -> None:
        """Disable telemetry collection."""
        self.config.enabled = False
        if posthog:
            posthog.disabled = True
        logger.info("Telemetry disabled")
        if self.config.project_root:
            self._setup_local_storage()


# Global telemetry client instance
_client: Optional[PostHogTelemetryClient] = None


def get_posthog_telemetry_client(project_root: Optional[Path] = None) -> PostHogTelemetryClient:
    """Get or initialize the global PostHog telemetry client.

    Args:
        project_root: Root directory of the project

    Returns:
        The global telemetry client instance
    """
    global _client

    if _client is None:
        _client = PostHogTelemetryClient(project_root)

    return _client


def disable_telemetry() -> None:
    """Disable telemetry collection globally."""
    if _client is not None:
        _client.disable()
