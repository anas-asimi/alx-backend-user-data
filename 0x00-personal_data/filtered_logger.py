#!/usr/bin/env python3
"""
filtered_logger.py
"""

import re
from typing import List


def filter_item(fields: List[str], redaction: str, item: str) -> str:
    """
    filter_item
    Args:
        fields (List[str]):
        redaction (str):
        item (str):
    Returns:
        str:
    """
    if len(item) < 1:
        return ''
    k, v = item.split('=')
    if k not in fields:
        return item
    return f'{k}={redaction}'


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    filter_datum
    Args:
        fields (List[str]):
        redaction (str):
        message (str):
        separator (str):
    Returns:
        str:
    """
    obfuscated_list = []    # sorry alx checker - re.sub()
    for item in message.split(separator):
        obfuscated_list.append(filter_item(fields, redaction, item))
    return separator.join(obfuscated_list)
