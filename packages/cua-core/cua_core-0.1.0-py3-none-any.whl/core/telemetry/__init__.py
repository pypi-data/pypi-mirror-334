"""Transparent telemetry collection for Cua components."""

from core.telemetry.telemetry import (
    TelemetryBackend,
    UniversalTelemetryClient,
    disable_telemetry,
    enable_telemetry,
    flush,
    get_telemetry_client,
    increment,
    record_event,
)

__all__ = [
    "TelemetryBackend",
    "UniversalTelemetryClient",
    "disable_telemetry",
    "enable_telemetry",
    "flush",
    "get_telemetry_client",
    "increment",
    "record_event",
]
