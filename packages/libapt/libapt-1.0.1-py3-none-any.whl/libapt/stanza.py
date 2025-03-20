"""
Process stanzas used by APT metadata.
"""

import logging

from typing import Any


def stanza_to_dict(lines: list[str], stop_on_empty_line: bool = True) -> dict[str, Any]:
    """
    Convert APT stanza metadata to a Python dict.

    :param lines: Lines of the stanza.
    :param stop_on_empty_line: Stop processing on empty line, i.e. after first stanza.
    :return: Dict containing stanza data.
    """
    data = {}

    key = None
    content = ""

    for line in lines:
        if not line.strip():
            if stop_on_empty_line:
                break
            else:
                continue

        if line.startswith(" ") or line.startswith("\t"):
            # Continuation of previous value.
            content += "\n" + line.strip()
        else:
            if key is not None:
                data[key] = content
                key = None
                content = ""
            elif content.strip():
                logging.warning("Content %s of stanza %s is dropped because key is missing.", content, lines)

            parts = line.split(":", maxsplit=1)
            key = parts[0].strip().replace("-", "_")
            content = parts[1].strip()
    if key:  # pragma: no cover
        data[key] = content

    return data


def stanzas_to_list(content: str) -> list[dict[str, Any]]:
    """
    Convert APT stanzas metadata to a list of Python dicts.

    :param content: Content of the stanzas.
    :return: List of dicts containing stanza data.
    """
    data: list[dict[str, Any]] = []
    for stanza in content.split("\n\n"):
        stanza = stanza.strip()
        if stanza != "":
            data.append(stanza_to_dict(stanza.split("\n")))
    return data
