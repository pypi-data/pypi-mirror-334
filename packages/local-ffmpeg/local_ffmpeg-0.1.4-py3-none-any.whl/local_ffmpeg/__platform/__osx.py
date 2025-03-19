"""
macOS-specific implementation for FFmpeg installation
"""

import os
import platform
import shutil
import subprocess
import zipfile
from typing import Optional, Dict

__all__ = ["MacOSHandler"]


class MacOSHandler:
    """Handler for macOS platform"""

    def get_download_url(self) -> Dict[str, str]:
        """
        Get the appropriate FFmpeg download URLs for macOS

        Returns:
            Dictionary with URLs for each binary (ffmpeg, ffplay, ffprobe)

        Raises:
            RuntimeError: Unsupported macOS architecture
        """
        # Get system architecture
        arch = platform.machine()

        # Map architecture to appropriate URL format
        if arch == "x86_64":
            arch_name = "intel"
        elif arch == "arm64":
            arch_name = "arm"
        else:
            raise RuntimeError(f"Unsupported macOS architecture: {arch}")

        # Return URLs for each binary (using version 7.1)
        return {
            "ffmpeg": f"https://www.osxexperts.net/ffmpeg71{arch_name}.zip",
            "ffplay": f"https://www.osxexperts.net/ffplay71{arch_name}.zip",
            "ffprobe": f"https://www.osxexperts.net/ffprobe71{arch_name}.zip",
        }

    def install(self, download_path: str, install_path: str) -> None:
        """
        Install FFmpeg on macOS using osxexperts.net builds

        Args:
            download_path: Path to the directory containing downloaded archives
            install_path: Directory where FFmpeg binaries will be installed
        """
        # Create installation directory if it doesn't exist
        os.makedirs(install_path, exist_ok=True)

        try:
            # Get download URLs for all binaries
            urls = self.get_download_url()

            # Process each binary
            for binary in ["ffmpeg", "ffplay", "ffprobe"]:
                binary_zip = os.path.join(download_path, f"{binary}.zip")

                # Extract the binary from the zip file
                with zipfile.ZipFile(binary_zip, "r") as zip_ref:
                    # List files in the archive
                    file_list = zip_ref.namelist()

                    # The archive should contain a single file (the binary)
                    if len(file_list) != 1:
                        print(f"Warning: Expected 1 file in {binary} archive, found {len(file_list)}")

                    # Extract the binary to the installation path
                    for file_name in file_list:
                        # Extract and rename to standard binary name
                        zip_ref.extract(file_name, path=install_path)
                        extracted_path = os.path.join(install_path, file_name)
                        target_path = os.path.join(install_path, binary)

                        # Rename if necessary
                        if os.path.basename(extracted_path) != binary:
                            os.rename(extracted_path, target_path)

                # Make binary executable
                binary_path = os.path.join(install_path, binary)
                if os.path.exists(binary_path):
                    os.chmod(binary_path, 0o755)

            print(f"FFmpeg has been installed to {install_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to install FFmpeg: {str(e)}")

    def uninstall(self, install_path: str) -> None:
        """
        Uninstall FFmpeg from macOS

        Args:
            install_path: Directory where FFmpeg binaries are installed
        """
        if os.path.exists(install_path):
            try:
                # Remove the binaries
                for binary in ["ffmpeg", "ffplay", "ffprobe"]:
                    binary_path = os.path.join(install_path, binary)
                    if os.path.exists(binary_path):
                        os.remove(binary_path)

                # Remove directory if empty
                if not os.listdir(install_path):
                    os.rmdir(install_path)

                print(f"FFmpeg has been uninstalled from {install_path}")

            except Exception as e:
                raise RuntimeError(f"Failed to uninstall FFmpeg: {str(e)}")
        else:
            print(f"FFmpeg installation not found at {install_path}")

    def check_installed(self, path: Optional[str] = None) -> bool:
        # Check in specified path if provided
        if path and os.path.exists(path):
            missing = []
            for binary in ("ffmpeg", "ffprobe", "ffplay"):
                binary_path = os.path.join(path, binary)
                if not (os.path.exists(binary_path) and os.access(binary_path, os.X_OK)):
                    missing.append(binary)
            if missing:
                print("Missing binaries:", ", ".join(missing))
                return False
            for binary in ("ffmpeg", "ffprobe", "ffplay"):
                binary_path = os.path.join(path, binary)
                try:
                    result = subprocess.run(
                        [binary_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5
                    )
                    if result.returncode != 0:
                        print(f"Binary {binary} exists but returned error code {result.returncode}.")
                        return False
                except (subprocess.SubprocessError, OSError) as e:
                    print(f"Error while executing {binary}: {e}")
                    return False
            return True

        # Global check if path is not provided
        for binary in ("ffmpeg", "ffprobe", "ffplay"):
            try:
                result = subprocess.run([binary, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                if result.returncode != 0:
                    print(f"Global binary {binary} returned error code {result.returncode}.")
                    return False
            except (subprocess.SubprocessError, OSError) as e:
                print(f"Error while executing global binary {binary}: {e}")
                return False
        return True
