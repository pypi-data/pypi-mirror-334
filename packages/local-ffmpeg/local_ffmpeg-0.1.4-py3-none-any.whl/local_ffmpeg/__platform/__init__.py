"""
Platform detection and handler selection
"""

import platform
import sys

__all__ = ["get_platform_handler"]


def get_platform_handler():
    """
    Detect the current platform and return the appropriate platform handler

    Returns:
        Platform-specific handler object

    Raises:
        RuntimeError: If the platform is not supported
    """
    system = platform.system().lower()

    if system == "windows":
        from local_ffmpeg.__platform.__win import WindowsHandler

        return WindowsHandler()

    elif system == "linux":
        from local_ffmpeg.__platform.__linux import LinuxHandler

        return LinuxHandler()

    elif system == "darwin":
        from local_ffmpeg.__platform.__osx import MacOSHandler

        return MacOSHandler()

    else:
        raise RuntimeError(f"Unsupported platform: {system}")
