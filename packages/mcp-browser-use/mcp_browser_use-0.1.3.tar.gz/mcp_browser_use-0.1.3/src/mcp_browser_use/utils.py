# ruff: noqa: E402

import asyncio
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_playwright_installation():
    """
    Check if Playwright is installed and properly set up.
    Returns:
        bool: True if Playwright is installed, False otherwise
    """
    try:
        # Try to import playwright to check if it's installed
        import playwright

        # Check if browsers are installed
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Try to launch a browser to verify installation
                browser = p.chromium.launch(headless=True)
                browser.close()
            return True
        except Exception as e:
            if "Executable doesn't exist" in str(e):
                logger.error("Playwright browsers are not installed. Installing now...")
                try:
                    subprocess.run(
                        [sys.executable, "-m", "playwright", "install", "chromium"],
                        check=True,
                    )
                    logger.info("Playwright browsers installed successfully.")
                    return True
                except subprocess.CalledProcessError:
                    logger.error(
                        "Failed to install Playwright browsers. Please run 'playwright install' manually."
                    )
                    return False
            else:
                logger.error(f"Error checking Playwright installation: {e}")
                return False
    except ImportError:
        logger.error(
            "Playwright is not installed. Please install it with 'pip install playwright'"
        )
        return False
