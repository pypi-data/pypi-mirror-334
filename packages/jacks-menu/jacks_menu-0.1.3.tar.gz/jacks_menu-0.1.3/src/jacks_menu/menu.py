#!/usr/bin/env python3
"""A data structure encoding the menu."""

from dataclasses import dataclass


@dataclass
class Menu:
    """Dataclass containing the menu date and items."""

    location: str
    web: str
    date: str
    items: list[str]
