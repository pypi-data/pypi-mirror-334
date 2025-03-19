#!/usr/bin/env python3
"""Test the menu parser."""

from pathlib import Path

import pytest

from jacks_menu.parser import parse_menu

TEST_MENU_DIRECTORY = Path(__file__).parent / "test_menus"


@pytest.mark.parametrize("menu_file", list(TEST_MENU_DIRECTORY.iterdir()))
def test_parse_menu(menu_file: Path) -> None:
    """Test that valid menus can be parsed without error."""
    menu_text = menu_file.read_text()
    parse_menu("location", "url", menu_text)
