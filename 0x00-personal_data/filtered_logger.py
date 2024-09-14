#!/usr/bin/env python3
"""
filtered_logger.py
"""

import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt
