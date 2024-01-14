#!/usr/bin/env python3
"""Filtered Logger
This script contains a function that
returns the log message obuscated
"""

import logging
import re
from typing import List
import mysql.connector
import os


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """FILTER DATUM
    This function returns the log message obfuscated

    PARAMETERS:
    @fields: a list of strings representing all fields to obfuscate
    @redaction: a string representing by what the field will be obfuscated
    @message: a string representing the log line
    @separator: a string representing by which character is separating all
    fields in the log line (message)

    RETURN VALUE
    The obfuscated string
    """
    obfuscated_message: str = message
    for field in fields:
        pattern: str = rf"(?<={field}=)[a-zA-Z0-9\/.-]*(?={separator})"
        obfuscated_message = re.sub(pattern, redaction, obfuscated_message)
    return obfuscated_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """"""
        self.fields: List[str] = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """This method formats the logging record object
        and returns the formated string obfuscated
        """
        formatter: logging.Formatter = logging.Formatter(RedactingFormatter.FORMAT)
        message: str = filter_datum(
            self.fields, RedactingFormatter.REDACTION,
            formatter.format(record), RedactingFormatter.SEPARATOR)
        return message


# PII_FIELDS = ("ssn", "password", "phone", "name", "email")


# def get_logger() -> logging.Logger:
#     """get_logger
#     A function that takes no arguments and returns a logging.Logger object.
#     """
#     logger = logging.getLogger("user_data")

#     # Set the logging level
#     logger.setLevel(logging.INFO)

#     # Create a stream handler
#     stream_handler = logging.StreamHandler()

#     # Set the logging level
#     stream_handler.setLevel(logging.INFO)

#     # Set the logging formatter and add the stream handler
#     # to the logger
#     stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
#     logger.addHandler(stream_handler)

#     return logger


# def get_db() -> mysql.connector.connection.MySQLConnection:
#     """get_db
#     This function connects to a secure database to read
#     a particular table. The database is protected by a
#     username and password that are set as environment
#     variables
#     """
#     db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME")
#     db_host = os.environ.get("PERSONAL_DATA_DB_HOST")
#     db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
#     password = os.environ.get("PERSONAL_DATA_DB_PASSWORD")

#     cnx = mysql.connector.connect(
#         user=db_username, host=db_host,
#         password=password, database=db_name
#     )
#     return cnx


# def main():
#     """This function runs when the script is run"""
#     cnx = get_db()
#     cursor = cnx.cursor()
#     cursor.execute("SELECT * FROM users;")
#     message = ""
#     log_record = []


# if __name__ == "__main__":
#     main()
