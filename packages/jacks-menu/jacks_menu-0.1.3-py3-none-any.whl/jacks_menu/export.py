#!/usr/bin/env python3
"""Logic to export the menu as a markdown file."""

from jacks_menu.constants import DATE, NOW
from jacks_menu.menu import Menu

HEADER = f"""---
title: "Jack's Gelato Menus"
author: "Edmund Goodman"
date: {NOW}
---

"""

FOOTER = """All menu information is property of Jack's Gelato. This page is
updated daily at 10:20am -- see my
[blog post]({{< ref "/posts/a_faster_gelato" >}}) for why I made it.
"""

ERROR_MESSAGE = (
    "Oops! Something went wrong with either retrieving or parsing the menu."
    " This will probably magically fix itself tomorrow.\n\n"
    "In the meantime, you can click on the heading link to go to the real menu."
)


def markdown_wrap_contents(location: str, web: str, date: str, contents: str) -> str:
    """Wrap the markdown contents with a subheading.

    Args:
        location: The location of the menu.
        web: The link back to the real menu site.
        date: The date of the menu.
        contents: The contents of the menu text (items or error message).

    Returns:
        A markdown representation of the menu data.
    """
    return f"## [{location}]({web}) ({date})\n\n{contents}\n\n"


def get_menu_markdown(menu: Menu) -> str:
    """Get a markdown representation of the menu."""
    return markdown_wrap_contents(
        menu.location,
        menu.web,
        menu.date,
        "\n".join(f"- {item}" for item in menu.items),
    )


def get_error_markdown(location: str, web: str) -> str:
    """Get a markdown representation of the error."""
    return markdown_wrap_contents(location, web, DATE, ERROR_MESSAGE)


def get_blog_markdown(menus_markdown: dict[str, str]) -> str:
    """Get the markdown for the blog containing all menus."""
    joined_menus_markdown = "\n".join(menus_markdown.values())
    return f"{HEADER}{joined_menus_markdown}{FOOTER}"
