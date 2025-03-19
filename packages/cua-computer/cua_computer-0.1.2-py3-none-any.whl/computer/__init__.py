"""CUA Computer Interface for cross-platform computer control."""

__version__ = "0.1.0"

# Initialize telemetry when the package is imported
try:
    from core.telemetry import enable_telemetry, set_dimension

    # Enable telemetry by default
    enable_telemetry()
    # Set the package version as a dimension
    set_dimension("computer_version", __version__)
except ImportError:
    # Core telemetry not available
    pass

from .computer import Computer

__all__ = ["Computer"]
