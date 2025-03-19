"""Computer telemetry for tracking anonymous usage and feature usage."""

import logging
import platform
from typing import Dict, Any, Optional

# Import the core telemetry module
try:
    from core.telemetry import record_event, increment_counter, set_dimension, get_telemetry_client

    TELEMETRY_AVAILABLE = True
except ImportError:
    TELEMETRY_AVAILABLE = False


# Local fallbacks in case core telemetry isn't available
def _noop(*args: Any, **kwargs: Any) -> None:
    """No-op function for when telemetry is not available."""
    pass


logger = logging.getLogger("cua.computer.telemetry")

# If telemetry isn't available, use no-op functions
if not TELEMETRY_AVAILABLE:
    logger.debug("Telemetry not available, using no-op functions")
    record_event = _noop  # type: ignore
    increment_counter = _noop  # type: ignore
    set_dimension = _noop  # type: ignore
    get_telemetry_client = lambda: None  # type: ignore

# Get system info once to use in telemetry
SYSTEM_INFO = {
    "os": platform.system().lower(),
    "os_version": platform.release(),
    "python_version": platform.python_version(),
}


def record_computer_initialization() -> None:
    """Record when a computer instance is initialized."""
    if TELEMETRY_AVAILABLE:
        record_event("computer_initialized", SYSTEM_INFO)

        # Set dimensions that will be attached to all events
        set_dimension("os", SYSTEM_INFO["os"])
        set_dimension("os_version", SYSTEM_INFO["os_version"])
        set_dimension("python_version", SYSTEM_INFO["python_version"])


def record_computer_action(
    action_type: str, success: bool, duration_ms: Optional[float] = None
) -> None:
    """Record when a computer action is performed.

    Args:
        action_type: The type of action (click, key, etc.)
        success: Whether the action was successful
        duration_ms: The duration of the action in milliseconds
    """
    if TELEMETRY_AVAILABLE:
        properties: Dict[str, Any] = {"action_type": action_type, "success": success, **SYSTEM_INFO}
        if duration_ms is not None:
            properties["duration_ms"] = duration_ms

        record_event("computer_action", properties)
        increment_counter(f"computer_action_{action_type}")

        # Increment success/failure counters
        if success:
            increment_counter("computer_actions_success")
        else:
            increment_counter("computer_actions_failure")
