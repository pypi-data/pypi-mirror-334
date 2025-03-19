"""Computer telemetry for tracking anonymous usage and feature usage."""

import logging
import os
import platform
import sys
import time
from typing import Dict, Any, Optional

# Import the core telemetry module
TELEMETRY_AVAILABLE = False

try:
    from core.telemetry import (
        record_event,
        increment,
        get_telemetry_client,
        flush,
        is_telemetry_enabled,
        is_telemetry_globally_disabled,
    )

    def increment_counter(counter_name: str, value: int = 1) -> None:
        """Wrapper for increment to maintain backward compatibility."""
        if is_telemetry_enabled():
            increment(counter_name, value)

    def set_dimension(name: str, value: Any) -> None:
        """Set a dimension that will be attached to all events."""
        logger = logging.getLogger("cua.computer.telemetry")
        logger.debug(f"Setting dimension {name}={value}")

    TELEMETRY_AVAILABLE = True
    logger = logging.getLogger("cua.computer.telemetry")
    logger.info("Successfully imported telemetry")
except ImportError as e:
    logger = logging.getLogger("cua.computer.telemetry")
    logger.warning(f"Could not import telemetry: {e}")
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
    flush = _noop  # type: ignore
    is_telemetry_enabled = lambda: False  # type: ignore
    is_telemetry_globally_disabled = lambda: True  # type: ignore

# Get system info once to use in telemetry
SYSTEM_INFO = {
    "os": platform.system().lower(),
    "os_version": platform.release(),
    "python_version": platform.python_version(),
}


def enable_telemetry() -> bool:
    """Enable telemetry if available.

    Returns:
        bool: True if telemetry was successfully enabled, False otherwise
    """
    global TELEMETRY_AVAILABLE

    # Check if globally disabled using core function
    if TELEMETRY_AVAILABLE and is_telemetry_globally_disabled():
        logger.info("Telemetry is globally disabled via environment variable - cannot enable")
        return False

    # Already enabled
    if TELEMETRY_AVAILABLE:
        return True

    # Try to import and enable
    try:
        from core.telemetry import (
            record_event,
            increment,
            get_telemetry_client,
            flush,
            is_telemetry_globally_disabled,
        )

        # Check again after import
        if is_telemetry_globally_disabled():
            logger.info("Telemetry is globally disabled via environment variable - cannot enable")
            return False

        TELEMETRY_AVAILABLE = True
        logger.info("Telemetry successfully enabled")
        return True
    except ImportError as e:
        logger.warning(f"Could not enable telemetry: {e}")
        return False


def disable_telemetry() -> None:
    """Disable telemetry for this session."""
    global TELEMETRY_AVAILABLE
    TELEMETRY_AVAILABLE = False
    logger.info("Telemetry disabled for this session")


def is_telemetry_enabled() -> bool:
    """Check if telemetry is enabled.

    Returns:
        bool: True if telemetry is enabled, False otherwise
    """
    # Use the core function if available, otherwise use our local flag
    if TELEMETRY_AVAILABLE:
        from core.telemetry import is_telemetry_enabled as core_is_enabled

        return core_is_enabled()
    return False


def record_computer_initialization() -> None:
    """Record when a computer instance is initialized."""
    if TELEMETRY_AVAILABLE and is_telemetry_enabled():
        record_event("computer_initialized", SYSTEM_INFO)

        # Set dimensions that will be attached to all events
        set_dimension("os", SYSTEM_INFO["os"])
        set_dimension("os_version", SYSTEM_INFO["os_version"])
        set_dimension("python_version", SYSTEM_INFO["python_version"])


def categorize_action(action_type: str) -> str:
    """Categorize the action based on the method name.

    Args:
        action_type: The method name/action type to categorize

    Returns:
        str: Category of the action (mouse, keyboard, etc.)
    """
    action_type = action_type.lower()

    if any(
        keyword in action_type
        for keyword in ["mouse", "click", "move", "drag", "position", "scroll"]
    ):
        return "mouse"
    elif any(keyword in action_type for keyword in ["key", "type", "press", "hotkey", "keyboard"]):
        return "keyboard"
    elif any(keyword in action_type for keyword in ["clipboard", "paste", "copy"]):
        return "clipboard"
    elif any(keyword in action_type for keyword in ["file", "directory", "folder", "path"]):
        return "filesystem"
    elif "scroll" in action_type:
        return "scroll"
    elif any(
        keyword in action_type for keyword in ["run", "stop", "start", "connect", "disconnect"]
    ):
        return "lifecycle"
    elif any(
        keyword in action_type for keyword in ["screen", "screenshot", "display", "resolution"]
    ):
        return "screen"
    elif any(keyword in action_type for keyword in ["command", "execute", "shell", "terminal"]):
        return "command"
    else:
        return "other"


def record_computer_action(
    action_type: str,
    status: str = "complete",
    args: Any = None,
    kwargs: Any = None,
    result: Any = None,
    duration: Optional[float] = None,
    success: bool = True,
    error_type: Optional[str] = None,
    computer: Any = None,
) -> None:
    """Record computer actions in telemetry for analytics.

    Args:
        action_type: The type of action (method name)
        status: Status of the action (start, complete, error)
        args: Arguments passed to the method (will be stringified)
        kwargs: Keyword arguments passed to the method (will be stringified)
        result: Result of the method call (will be stringified)
        duration: Duration of the action in seconds
        success: Whether the action was successful
        error_type: Type of error if the action failed
        computer: Computer instance that performed the action
    """
    # Skip if telemetry is globally disabled
    if not is_telemetry_enabled():
        return

    # Skip internal methods
    if action_type.startswith("_"):
        return

    # Prepare properties for the telemetry event
    properties: Dict[str, Any] = {
        "action_type": action_type,
        "status": status,
        "success": success,
    }

    # Add action category
    properties["action_category"] = categorize_action(action_type)

    # Add error information if applicable
    if not success and error_type:
        properties["error_type"] = error_type

    # Add duration if available
    if duration is not None:
        properties["duration_seconds"] = duration

    # Add system information
    properties["os"] = sys.platform
    properties["python_version"] = platform.python_version()

    # Collect minimal info about arguments if verbose logging is enabled
    if os.environ.get("CUA_VERBOSE_TELEMETRY", "").lower() in ("1", "true", "yes", "on"):
        # Only include argument counts for privacy
        if args:
            properties["arg_count"] = len(args)
        if kwargs:
            properties["kwarg_count"] = len(kwargs)

        # For debugging and privacy reasons, only log result type and size
        if result is not None:
            result_type = type(result).__name__
            properties["result_type"] = result_type

            # For collection types, add their size
            if hasattr(result, "__len__"):
                try:
                    properties["result_size"] = len(result)
                except (TypeError, ValueError):
                    pass

    # Record the event
    record_event("computer_action", properties)
