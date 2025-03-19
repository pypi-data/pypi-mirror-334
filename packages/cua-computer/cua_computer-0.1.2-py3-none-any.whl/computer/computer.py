from typing import Optional, List, Literal, Dict, Any, Union
from pylume import PyLume, VMRunOpts, SharedDirectory
import asyncio
from .models import Computer as ComputerConfig, Image, Display
from .interface.factory import InterfaceFactory
from pylume import ImageRef, VMUpdateOpts, PyLume
import time
from PIL import Image
import io
from .utils import bytes_to_image
import re
from .logger import Logger, LogLevel
import json
from pylume.models import VMRunOpts, VMUpdateOpts, ImageRef, SharedDirectory, VMStatus
import logging
from .telemetry import (
    record_computer_initialization,
    record_computer_action,
)

OSType = Literal["macos", "linux"]


class Computer:
    """Main computer interface."""

    def __init__(
        self,
        display: Union[Display, Dict[str, int], str] = "1024x768",
        memory: str = "8GB",
        cpu: str = "4",
        os: OSType = "macos",
        name: str = "",
        image: str = "macos-sequoia-cua:latest",
        shared_directories: Optional[List[str]] = None,
        use_host_computer_server: bool = False,
        verbosity: Union[int, LogLevel] = logging.INFO,
    ):
        """Initialize a new Computer instance.

        Args:
            display: The display configuration. Can be:
                    - A Display object
                    - A dict with 'width' and 'height'
                    - A string in format "WIDTHxHEIGHT" (e.g. "1920x1080")
                    Defaults to "1024x768"
            memory: The VM memory allocation. Defaults to "8GB"
            cpu: The VM CPU allocation. Defaults to "4"
            os: The operating system type ('macos' or 'linux')
            name: The VM name
            image: The VM image name
            shared_directories: Optional list of directory paths to share with the VM
            use_host_computer_server: If True, target localhost instead of starting a VM
            verbosity: Logging level (standard Python logging levels: logging.DEBUG, logging.INFO, etc.)
                      LogLevel enum values are still accepted for backward compatibility
        """
        self.logger = Logger("cua.computer", verbosity)
        self.logger.info("Initializing Computer...")

        # Store original parameters
        self.image = image

        # Set initialization flag
        self._initialized = False
        self._running = False

        # Configure root logger
        self.verbosity = verbosity
        self.logger = Logger("cua", verbosity)

        # Configure component loggers with proper hierarchy
        self.vm_logger = Logger("cua.vm", verbosity)
        self.interface_logger = Logger("cua.interface", verbosity)

        if not use_host_computer_server:
            if ":" not in image or len(image.split(":")) != 2:
                raise ValueError("Image must be in the format <image_name>:<tag>")

            if not name:
                # Normalize the name to be used for the VM
                name = image.replace(":", "_")

            # Convert display parameter to Display object
            if isinstance(display, str):
                # Parse string format "WIDTHxHEIGHT"
                match = re.match(r"(\d+)x(\d+)", display)
                if not match:
                    raise ValueError(
                        "Display string must be in format 'WIDTHxHEIGHT' (e.g. '1024x768')"
                    )
                width, height = map(int, match.groups())
                display_config = Display(width=width, height=height)
            elif isinstance(display, dict):
                display_config = Display(**display)
            else:
                display_config = display

            self.config = ComputerConfig(
                image=image.split(":")[0],
                tag=image.split(":")[1],
                name=name,
                display=display_config,
                memory=memory,
                cpu=cpu,
            )
            # Initialize PyLume but don't start the server yet - we'll do that in run()
            self.config.pylume = PyLume(
                debug=(self.verbosity == LogLevel.DEBUG),
                port=3000,
                use_existing_server=False,
                server_start_timeout=120,  # Increase timeout to 2 minutes
            )

        self._interface = None
        self.os = os
        self.shared_paths = []
        if shared_directories:
            for path in shared_directories:
                abs_path = os.path.abspath(os.path.expanduser(path))  # type: ignore[attr-defined]
                if not os.path.exists(abs_path):  # type: ignore[attr-defined]
                    raise ValueError(f"Shared directory does not exist: {path}")
                self.shared_paths.append(abs_path)
        self._pylume_context = None
        self.use_host_computer_server = use_host_computer_server

        # Record initialization in telemetry
        record_computer_initialization()

    async def __aenter__(self):
        """Enter async context manager."""
        await self.run()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager."""
        # await self.stop()
        pass

    async def run(self) -> None:
        """Start the computer."""

        start_time = time.time()
        success = True

        try:
            # If using host computer server
            if self.use_host_computer_server:
                self.logger.info("Using host computer server (no VM needed)")
                self._interface = InterfaceFactory.create("http", "localhost", 8000, self.logger)
                self._running = True
                self.logger.info("Host computer server initialized.")
                return

            self.logger.info("Starting computer...")

            if not hasattr(self, "_pylume"):
                self._pylume = PyLume()

            if not self._vm_name:
                # No name given, use a random name
                self._vm_name = "cua-" + str(time.time()).replace(".", "-")

            # Start the VM
            opts = VMRunOpts(
                image=self._image,
                cpu=self._cpu,
                memory=self._memory,
                display=self._display,
            )

            # Add shared directories if configured
            if self._shared_dirs:
                opts.shared_directories = []
                for dir_path in self._shared_dirs:
                    opts.shared_directories.append(SharedDirectory(host_path=dir_path))

            if hasattr(self, "_vm"):
                # Already have a VM - make sure it's running
                if not await self._vm.is_running():
                    await self._vm.start()
            else:
                self.logger.info(
                    f"Launching VM '{self._vm_name}' with {self._cpu} CPU, "
                    f"{self._memory} memory, {self._display['width']}x{self._display['height']} display"
                )
                self._vm = await self._pylume.run_vm(self._vm_name, opts)

            # Get IP address
            self.logger.debug("Waiting for VM to be ready...")
            status = await self.wait_vm_ready()

            # Preload the ip to avoid future blocking method calls
            self._ip = (
                status["ip"] if isinstance(status, dict) and "ip" in status else await self._vm.ip()
            )

            # Create the interface
            self._interface = InterfaceFactory.create("http", self._ip, 8000, self.logger)
            self._running = True
            # Setup the stop event
            self._stop_event = asyncio.Event()

            # Add any shared directories to the guest
            await self._setup_shared_directories()

            self.logger.info("Computer successfully initialized")
            return
        except Exception as e:
            success = False
            raise
        finally:
            # Record the action in telemetry
            duration_ms = (time.time() - start_time) * 1000
            record_computer_action("run", success, duration_ms)

    async def stop(self) -> None:
        """Stop the computer."""

        start_time = time.time()
        success = True

        try:
            if not hasattr(self, "_running") or not self._running:
                self.logger.info("Computer is not running, nothing to stop")
                return

            self._running = False
            self.logger.info("Stopping Computer...")

            # Stop the VM if it's running
            if not self.use_host_computer_server and hasattr(self, "_vm"):
                try:
                    await self._vm.stop()
                    self.logger.info("VM stopped successfully")
                except Exception as e:
                    self.logger.debug(f"Error stopping VM: {e}")

            # Clear the interface reference
            self._interface = None

            self.logger.info("Computer stopped successfully")
        except Exception as e:
            success = False
            self.logger.debug(f"Error during cleanup: {e}")
            raise
        finally:
            # Record the action in telemetry
            duration_ms = (time.time() - start_time) * 1000
            record_computer_action("stop", success, duration_ms)

    # @property
    async def get_ip(self) -> str:
        """Get the IP address of the VM or localhost if using host computer server."""
        if self.use_host_computer_server:
            return "127.0.0.1"
        ip = await self.config.get_ip()
        return ip or "unknown"  # Return "unknown" if ip is None

    async def wait_vm_ready(self) -> Optional[Union[Dict[str, Any], "VMStatus"]]:
        """Wait for VM to be ready with an IP address.

        Returns:
            VM status information or None if using host computer server.
        """
        if self.use_host_computer_server:
            return None

        timeout = 600  # 10 minutes timeout (increased from 4 minutes)
        interval = 2.0  # 2 seconds between checks (increased to reduce API load)
        start_time = time.time()
        last_status = None
        attempts = 0

        self.logger.info(f"Waiting for VM {self.config.name} to be ready (timeout: {timeout}s)...")

        while time.time() - start_time < timeout:
            attempts += 1
            elapsed = time.time() - start_time

            try:
                # Keep polling for VM info
                vm = await self.config.pylume.get_vm(self.config.name)  # type: ignore[attr-defined]

                # Log full VM properties for debugging (every 30 attempts)
                if attempts % 30 == 0:
                    self.logger.info(
                        f"VM properties at attempt {attempts}: {vars(vm) if vm else 'None'}"
                    )

                # Get current status for logging
                current_status = getattr(vm, "status", None) if vm else None
                if current_status != last_status:
                    self.logger.info(
                        f"VM status changed to: {current_status} (after {elapsed:.1f}s)"
                    )
                    last_status = current_status

                # Check for IP address - ensure it's not None or empty
                ip = getattr(vm, "ip_address", None) if vm else None
                if ip and ip.strip():  # Check for non-empty string
                    self.logger.info(
                        f"VM {self.config.name} got IP address: {ip} (after {elapsed:.1f}s)"
                    )
                    return vm

                if attempts % 10 == 0:  # Log every 10 attempts to avoid flooding
                    self.logger.info(
                        f"Still waiting for VM IP address... (elapsed: {elapsed:.1f}s)"
                    )
                else:
                    self.logger.debug(
                        f"Waiting for VM IP address... Current IP: {ip}, Status: {current_status}"
                    )

            except Exception as e:
                self.logger.warning(f"Error checking VM status (attempt {attempts}): {str(e)}")
                # If we've been trying for a while and still getting errors, log more details
                if elapsed > 60:  # After 1 minute of errors, log more details
                    self.logger.error(f"Persistent error getting VM status: {str(e)}")
                    self.logger.info("Trying to get VM list for debugging...")
                    try:
                        vms = await self.config.pylume.list_vms()  # type: ignore[attr-defined]
                        self.logger.info(
                            f"Available VMs: {[vm.name for vm in vms if hasattr(vm, 'name')]}"
                        )
                    except Exception as list_error:
                        self.logger.error(f"Failed to list VMs: {str(list_error)}")

            await asyncio.sleep(interval)

        # If we get here, we've timed out
        elapsed = time.time() - start_time
        self.logger.error(f"VM {self.config.name} not ready after {elapsed:.1f} seconds")

        # Try to get final VM status for debugging
        try:
            vm = await self.config.pylume.get_vm(self.config.name)  # type: ignore[attr-defined]
            status = getattr(vm, "status", "unknown") if vm else "unknown"
            ip = getattr(vm, "ip_address", None) if vm else None
            self.logger.error(f"Final VM status: {status}, IP: {ip}")
        except Exception as e:
            self.logger.error(f"Failed to get final VM status: {str(e)}")

        raise TimeoutError(
            f"VM {self.config.name} not ready after {elapsed:.1f} seconds - IP address not assigned"
        )

    async def update(self, cpu: Optional[int] = None, memory: Optional[str] = None):
        """Update VM settings."""
        self.logger.info(
            f"Updating VM settings: CPU={cpu or self.config.cpu}, Memory={memory or self.config.memory}"
        )
        update_opts = VMUpdateOpts(
            cpu=cpu or int(self.config.cpu), memory=memory or self.config.memory
        )
        await self.config.pylume.update_vm(self.config.image, update_opts)  # type: ignore[attr-defined]

    def get_screenshot_size(self, screenshot: bytes) -> Dict[str, int]:
        """Get the dimensions of a screenshot.

        Args:
            screenshot: The screenshot bytes

        Returns:
            Dict[str, int]: Dictionary containing 'width' and 'height' of the image
        """
        image = Image.open(io.BytesIO(screenshot))
        width, height = image.size
        return {"width": width, "height": height}

    @property
    def interface(self):
        """Get the computer interface for interacting with the VM.

        Returns:
            BaseComputerInterface: The interface for controlling the VM

        Raises:
            RuntimeError: If the interface is not initialized (run() not called)
        """
        if not hasattr(self, "_interface") or self._interface is None:
            error_msg = "Computer interface not initialized. Call run() first."
            self.logger.error(error_msg)
            self.logger.error(
                "Make sure to call await computer.run() before using any interface methods."
            )
            raise RuntimeError(error_msg)
        return self._interface

    def __getattr__(self, name: str):
        """Forward attribute access to the interface."""

        # For any method, try to get from interface with telemetry
        if hasattr(self.interface, name):
            original_method = getattr(self.interface, name)

            # Only wrap callables (methods)
            if callable(original_method):
                # Wrap the method with telemetry
                async def wrapped_method(*args, **kwargs):
                    start_time = time.time()
                    success = True

                    try:
                        result = await original_method(*args, **kwargs)
                        return result
                    except Exception as e:
                        success = False
                        raise
                    finally:
                        # Record the action in telemetry
                        duration_ms = (time.time() - start_time) * 1000
                        record_computer_action(name, success, duration_ms)

                return wrapped_method

            # If it's not callable, just return it directly
            return original_method

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    async def to_screen_coordinates(self, x: float, y: float) -> tuple[float, float]:
        """Convert normalized coordinates to screen coordinates.

        This is a convenience method that delegates to the interface.

        Args:
            x: X coordinate between 0 and 1
            y: Y coordinate between 0 and 1

        Returns:
            tuple[float, float]: Screen coordinates (x, y)
        """
        return await self.interface.to_screen_coordinates(x, y)

    async def to_screenshot_coordinates(self, x: float, y: float) -> tuple[float, float]:
        """Convert screen coordinates to screenshot coordinates.

        Args:
            x: X coordinate in screen space
            y: Y coordinate in screen space

        Returns:
            tuple[float, float]: (x, y) coordinates in screenshot space
        """
        screen_size = await self.interface.get_screen_size()
        screenshot = await self.interface.screenshot()
        screenshot_img = bytes_to_image(screenshot)
        screenshot_width, screenshot_height = screenshot_img.size

        # Calculate scaling factors
        width_scale = screenshot_width / screen_size["width"]
        height_scale = screenshot_height / screen_size["height"]

        # Convert coordinates
        screenshot_x = x * width_scale
        screenshot_y = y * height_scale

        return screenshot_x, screenshot_y
