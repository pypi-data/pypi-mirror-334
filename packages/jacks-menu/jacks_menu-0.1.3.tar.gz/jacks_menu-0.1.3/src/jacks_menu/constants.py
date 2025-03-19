#!/usr/bin/env python3
"""Constant values used by the tool."""

from datetime import datetime, timezone

NOW = datetime.now(timezone.utc)
DATE = datetime.strftime(NOW, "%y_%m_%d")

MENU_LOCATIONS: dict[str, str] = {
    "Bene't Street": "https://www.jacksgelato.com/bene-t-street-menu",
    "All Saints": "https://www.jacksgelato.com/all-saints-menu",
}

LOCATIONS_SANITISED: dict[str, str] = {
    "Bene't Street": "benet_street",
    "All Saints": "all_saints",
}

MENU_KNOWN_IDS: dict[str, str] = {
    "Bene't Street": "1dVYB7lnBgWE0bPhc9SFz0aLrkDfSCulrMctW1gDfCA8",
    "All Saints": "1kDBSxPb8X4L2TKXWUmm2A-VGuPVTyxmfbq9iwUQQ2nc",
}
