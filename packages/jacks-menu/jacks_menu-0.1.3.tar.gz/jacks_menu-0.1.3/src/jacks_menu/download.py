#!/usr/bin/env python3
"""Logic to retrieve the menu from the website."""

from pathlib import Path
from tempfile import NamedTemporaryFile

import gdown


class MenuRetrievalError(Exception):
    """Custom error for the menu retrieval operation failing."""


def get_menu_text(
    doc_id: str, output_file: Path | None = None, verbose: bool = False
) -> str:
    """Get the text content of menu given its Google doc id.

    Args:
        doc_id: The Google doc id to get the text content from.
        output_file: The output file to write the text content to, if set.
        verbose: Whether to show information about the download process.

    Raises:
        MenuRetrievalError: The menu text retrieval failed.

    Returns:
        The text content of menu given its Google doc id.
    """
    if output_file is not None and output_file.exists():
        if verbose:
            print(f"Output file '{output_file}' already exists.")
        return output_file.read_text()

    url = f"https://docs.google.com/uc?id={doc_id}"
    with NamedTemporaryFile() as tmp_handle:
        try:
            gdown.download(url, tmp_handle.name, format="txt", quiet=not verbose)
        except gdown.exceptions.FileURLRetrievalError as exc:
            raise MenuRetrievalError("Failed to retrieve menu text!") from exc
        menu_text = Path(tmp_handle.name).read_text()

    if output_file is not None:
        with output_file.open("w+") as output_handle:
            output_handle.write(menu_text)

    return menu_text
