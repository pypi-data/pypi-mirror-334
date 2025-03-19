#!/usr/bin/env python3
"""Logic to retrieve the document id from the website."""

from collections.abc import Generator
from contextlib import contextmanager
from re import match as re_match
from time import sleep
from typing import Any, TypeAlias

GOOGLE_DOC_PATTERN = r"https://docs.google.com/document/d/(.*)/preview"
WIX_DOC_ID = "11pi6xxtRoM2rF9XlgVhe46UQqCVbBrtqk2YBBwPkKN4"

FirefoxDriver: TypeAlias = Any


class MismatchedDocIdError(Exception):
    """Custom error for mismatched doc ids."""


class DocIdRetrievalError(Exception):
    """Custom error for failing to retrieve doc ids."""


@contextmanager
def headless_firefox_driver() -> Generator[FirefoxDriver, None, None]:
    """Context manager for a headless firefox driver."""
    try:
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from seleniumwire import webdriver
    except ModuleNotFoundError as err:
        raise RuntimeError(
            "Try installing the optional 'selenium' dependency group"
        ) from err

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_iframe_doc_id(
    url: str, expected_doc_id: str | None, verbose: bool = False
) -> str:
    """Get the Google doc id for a Jack's Gelato menu iFrame.

    Args:
        url: The URL of the menu webpage to get the doc url id from.
        expected_doc_id: The expected doc id to check against.
        verbose: Whether to show information about the retrieval process.

    Raises:
        MenuRetrievalError: The menu Google doc it retrieval failed.

    Returns:
        The Google doc url id.
    """
    with headless_firefox_driver() as driver:
        driver.get(url)

        # Because the wix google doc embedding is very silly, we need an
        # unconditional wait for >5 seconds, hence the `sleep(10)`
        driver.implicitly_wait(10)
        sleep(15)

        for request in driver.requests:
            if request.response:
                match = re_match(GOOGLE_DOC_PATTERN, request.url)
                if match and (doc_id := match.group(1)) != WIX_DOC_ID:
                    if verbose:
                        print(f"Retrieved doc id: {doc_id}")
                    if expected_doc_id and doc_id != expected_doc_id:
                        raise MismatchedDocIdError(
                            "Mismatched doc id!"
                            f" Expected '{expected_doc_id}', got '{doc_id}'"
                        )
                    return doc_id

    raise DocIdRetrievalError("Failed to retrieve menu Google doc id!")
