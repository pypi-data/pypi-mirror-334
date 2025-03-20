from typing import Dict, Any, Optional
import os
from ocular.api import OcularApiClient
from ocular.utils.errors import OcularError
from ocular.utils.logging import get_logger
import sys
import time
import requests
from urllib.parse import urljoin

logger = get_logger()


class Export:
    def __init__(
        self,
        export_info: Dict[str, Any],
        api_key: str,
    ):
        """
        Initialize an export instance.

        Args:
            export_info (Dict[str, Any]): Export information dictionary
            api_key (str): Ocular AI API key
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.id = export_info["id"]
        self.title = export_info["title"]
        self.creator = export_info["creator"]
        self.version = export_info["version"]
        self.format = export_info["format"]

        self.api_client = OcularApiClient(api_key)

    def download(
        self, target_path: Optional[str] = None, show_progress: bool = True
    ) -> str:
        """
        Download the export dataset as a zip file with progress display.

        Args:
            target_path (str, optional): Path where the file should be saved.
                                    If None, saves in current directory.
            show_progress (bool): Whether to display download progress.
                             Default is True.

        Returns:
            str: Path to the downloaded file
        """
        logger.info(f"Downloading export {self.id}")

        if not target_path:
            target_path = os.getcwd()

        default_filename = f"{self.id}.zip"

        if os.path.isdir(target_path):
            filename = os.path.join(target_path, default_filename)
        else:
            filename = target_path

        try:
            response = self.api_client.download_export(
                version_id=self.version["id"],
                export_id=self.id,
                stream=True,
            )

            total_size = int(response.headers.get("content-length", 0))

            if "Content-Disposition" in response.headers:
                cd = response.headers.get("Content-Disposition")
                if "filename=" in cd:
                    server_filename = cd.split("filename=")[1].strip('"')
                    if os.path.isdir(target_path):
                        filename = os.path.join(target_path, server_filename)

            if show_progress:
                last_percent = -1
                start_time = time.time()
                downloaded = 0

            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

                        if show_progress:
                            downloaded += len(chunk)

                            if total_size > 0:
                                percent = min(100, int((downloaded / total_size) * 100))

                                if percent > last_percent:
                                    last_percent = percent

                                    elapsed = time.time() - start_time
                                    speed = downloaded / elapsed if elapsed > 0 else 0

                                    current_mb = downloaded / (1024 * 1024)
                                    total_mb = total_size / (1024 * 1024)
                                    speed_mbps = speed / (1024 * 1024)

                                    bar_length = 30
                                    filled_length = int(bar_length * percent // 100)
                                    bar = "█" * filled_length + "░" * (
                                        bar_length - filled_length
                                    )

                                    sys.stdout.write(
                                        f"\rDownloading: [{bar}] {percent}% ({current_mb:.1f}/{total_mb:.1f} MB) {speed_mbps:.1f} MB/s"
                                    )
                                    sys.stdout.flush()
                            else:
                                downloaded_mb = downloaded / (1024 * 1024)
                                elapsed = time.time() - start_time
                                speed = downloaded / elapsed if elapsed > 0 else 0
                                speed_mbps = speed / (1024 * 1024)

                                sys.stdout.write(
                                    f"\rDownloading: {downloaded_mb:.1f} MB downloaded ({speed_mbps:.1f} MB/s)"
                                )
                                sys.stdout.flush()

            if show_progress:
                sys.stdout.write("\n")
                sys.stdout.flush()

            logger.info(f"Downloaded export to {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error downloading export: {str(e)}")
            if os.path.exists(filename):
                os.remove(filename)
            raise OcularError(f"Download failed: {str(e)}")
