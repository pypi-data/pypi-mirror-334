"""
Download module for FFmpeg binaries
"""

import os
import tempfile
import shutil
from typing import Optional, Dict, Union
import requests
from tqdm import tqdm


def download_url(url: Union[str, Dict[str, str]]) -> Optional[Union[str, Dict[str, str]]]:
    """
    Download FFmpeg binaries from the given URL or URLs

    Args:
        url: URL or dictionary of URLs to download FFmpeg from

    Returns:
        Path to the downloaded file(s), or None if download failed
    """
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp(prefix="local_ffmpeg_")

        # Handle both single URL and dictionary of URLs
        if isinstance(url, dict):
            # For macOS, we have separate URLs for each binary
            result = {}
            for binary, binary_url in url.items():
                # Determine filename from URL
                filename = os.path.basename(binary_url)
                temp_file = os.path.join(temp_dir, f"{binary}.zip")

                # Download file with progress bar
                response = requests.get(binary_url, stream=True)
                response.raise_for_status()

                total_size = int(response.headers.get("content-length", 0))

                with (
                    open(temp_file, "wb") as file,
                    tqdm(
                        desc=f"Downloading {filename}",
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar,
                ):
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
                        bar.update(len(data))

                result[binary] = temp_file

            return temp_dir  # Return directory path instead of individual files
        else:
            # Original single URL flow
            # Determine filename from URL
            filename = os.path.basename(url)
            temp_file = os.path.join(temp_dir, filename)

            # Download file with progress bar
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with (
                open(temp_file, "wb") as file,
                tqdm(
                    desc=f"Downloading {filename}",
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar,
            ):
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))

            return temp_file

    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
        if "temp_dir" in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return None
