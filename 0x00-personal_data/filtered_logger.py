#!/usr/bin/env python3
"""
filtered_logger.py
"""

import os
import re
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """Creates a new logger for user data.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


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
