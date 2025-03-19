# Cua Core

Core functionality shared across Cua components.

## Features

- Telemetry: Privacy-focused, transparent usage tracking
- Common utilities and shared functionality

## Installation

```bash
pip install cua-core
```

## Usage

### Telemetry

The telemetry system is designed with privacy in mind, collecting minimal data with user control:

```python
from cua.core.telemetry import get_telemetry_client, increment, record_event

# Simple API functions
increment("counter_name")
record_event("function_used", {"param1": "value1"})

# Or get the client for more control
client = get_telemetry_client()
client.record_event("function_name", {"param1": "value1"})
client.increment("counter_name")
client.disable()  # Disable telemetry
```

### Configuration

Telemetry can be configured through environment variables:

- `CUA_TELEMETRY=off` - Disable telemetry (enabled by default, opt-out)
- `CUA_TELEMETRY_SAMPLE_RATE=5` - Set sampling rate to 5% (default)

#### Telemetry Data Collection

By default, telemetry data is sent to our public PostHog instance, which allows us to improve the library based on usage patterns. We only collect anonymous, aggregated usage information with the following safeguards:

- Telemetry only collects anonymous usage information
- Data is anonymized using randomly generated IDs
- We only collect functional usage patterns, not user content
- Data is sampled to minimize the amount collected per user
- The collected data is publicly available in aggregated form

You can view our public telemetry dashboard at [https://eu.i.posthog.com](https://eu.i.posthog.com).

#### Privacy & Implementation

Our telemetry implementation prioritizes user privacy with a public, anonymous PostHog API key that:

- Only tracks functional usage (not user content)
- Creates random IDs not tied to user identities
- Applies sampling to minimize data collection
- Can be disabled by setting: `CUA_TELEMETRY=off`

For security reasons:
- API keys used are intentionally public and restricted to telemetry only
- All data is anonymized before collection
- The system is completely transparent about what is collected

## Development

```bash
# Install development dependencies
pdm install

# Run tests
pdm run pytest
```

## License

[License details] 