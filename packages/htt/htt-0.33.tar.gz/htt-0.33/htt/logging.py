import datetime
import json
import logging
import logging.handlers
import os
import queue
import re
import socket
import sys
from typing import Any

import logging_loki


def create_logger(
    name: str | None = None,
    stderr_enabled: bool = False,
    stderr_level: int = logging.NOTSET,
    file_enabled: bool = False,
    file_level: int = logging.NOTSET,
    file_name: str | None = None,
    file_size: int = 10,
    file_count: int = 30,
    syslog_enabled: bool = False,
    syslog_level: int = logging.NOTSET,
    syslog_address: str = "",
    syslog_socket_kind: socket.SocketKind = socket.SOCK_DGRAM,
    loki_enabled: bool = False,
    loki_level: int = logging.NOTSET,
    loki_endpoint: str = "",
    loki_user: str = "",
    loki_pass: str = "",
    loki_labels: dict[str, Any] = dict(),
):
    """Create logger with the specified handlers

    Args:
        name (Optional[str], optional): Logger name. Defaults to None.
        stderr_enabled (bool, optional): Enable logging to stderr. Defaults to False.
        stderr_level (int, optional): Logging level of stderr handler. Defaults to logging.NOTSET.
        file_enabled (bool, optional): Enable logging to file. Defaults to False.
        file_level (int, optional): Logging level of file handler. Defaults to logging.NOTSET.
        file_name (Optional[str], optional): File name of the log files. Defaults to None.
        file_size (int, optional): Rotation size of the log files in MB. Defaults to 10.
        file_count (int, optional): Rotation count of the log files. Defaults to 30.
        syslog_enabled (bool, optional): Enable logging to syslog. Defaults to False.
        syslog_level (int, optional): Logging level of syslog handler. Defaults to logging.NOTSET.
        syslog_address (str, optional): Address of the syslog server in "{ip}:{port}". Defaults to "".
        syslog_sockettype (socket.SocketKind, optional): Socket type of the syslog server. Defaults to socket.SOCK_DGRAM.
        loki_enabled (bool, optional): Enable logging to loki. Defaults to False.
        loki_level (int, optional): Logging level of loki handler. Defaults to logging.NOTSET.
        loki_endpoint (str, optional): Push endpoint of the loki server in "{protocol}://{ip}:{port}/loki/api/v1/push". Defaults to "".
        loki_user (str, optional): User of the loki server. Defaults to "".
        loki_pass (str, optional): Pass of the loki server. Defaults to "".
        loki_labels (dict[str, Any], optional): Labels describing the log stream. Defaults to empty.

    Returns:
        Logger: Logger created with specified handlers
    """
    logger = logging.getLogger(name=name)
    if name:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.NOTSET)
    if stderr_enabled:
        stderr_handler = _create_stderr_handler()
        stderr_handler.setLevel(stderr_level)
        logger.addHandler(stderr_handler)
    if file_enabled:
        if not file_name:
            raise ValueError("invalid file name")
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        file_handler = _create_file_handler(
            file_name,
            file_size,
            file_count,
        )
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)
    if syslog_enabled:
        if not syslog_address:
            raise ValueError("invalid syslog address")
        syslog_handler = _create_syslog_handler(
            syslog_address,
            syslog_socket_kind,
        )
        syslog_handler.setLevel(syslog_level)
        logger.addHandler(syslog_handler)
    if loki_enabled:
        if not loki_endpoint:
            raise ValueError("invalid loki endpoint")
        loki_handler = _create_loki_handler(
            loki_endpoint,
            loki_user,
            loki_pass,
            loki_labels,
        )
        loki_handler.setLevel(loki_level)
        logger.addHandler(loki_handler)
    return logger


def get_logger(
    name: str | None = None,
) -> logging.Logger:
    """Return a logger of the specified name. Logger must be created by create_logger() first.

    Args:
        name (Optional[str], optional): Logger name. Defaults to None.

    Returns:
        logging.Logger: Logger of the specified name
    """
    return logging.getLogger(name=name)


def _create_stderr_handler():
    formatter = _InlineFormatter()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    return handler


def _create_file_handler(
    file_name: str,
    file_size: int,
    file_count: int,
):
    formatter = _InlineFormatter()
    handler = logging.handlers.RotatingFileHandler(
        file_name,
        maxBytes=1048756 * file_size,
        backupCount=file_count,
        encoding="UTF-8",
    )
    handler.setFormatter(formatter)
    return handler


def _create_syslog_handler(
    syslog_address: str,
    syslog_socket_kind: socket.SocketKind,
):
    handler = logging.handlers.SysLogHandler(
        _split_address(syslog_address),
        socktype=syslog_socket_kind,
    )
    return handler


def _create_loki_handler(
    loki_endpoint: str,
    loki_user: str,
    loki_pass: str,
    loki_labels: dict[str, Any],
):
    formatter = _JsonFormatter()
    handler = logging_loki.LokiQueueHandler(
        queue.Queue(-1),
        url=loki_endpoint,
        auth=(loki_user, loki_pass) if loki_user else None,
        tags=loki_labels,
    )
    handler.setFormatter(formatter)
    return handler


def _split_address(address: str):
    match = re.match(r"^(.+):(\d+)$", address)
    if match:
        host = match.group(1)
        port = int(match.group(2))
    else:
        host = address
        port = None
    return (host, port)


class _DateTimeFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def formatTime(self, record, datefmt=None) -> str:
        ct = datetime.datetime.fromtimestamp(record.created, datetime.datetime.now().astimezone().tzinfo)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime(self.default_time_format)
        return s


class _LevelFormatter(logging.Formatter):
    default_formatter = _DateTimeFormatter
    default_notset_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_debug_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_info_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_warning_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_error_format = "%(levelname).1s %(asctime)s | %(message)s (%(module)s:%(lineno)d)"
    default_critical_format = "%(levelname).1s %(asctime)s | %(message)s (%(module)s:%(lineno)d)"

    def __init__(self, formats=None, **kwargs):
        if "fmt" in kwargs:
            raise ValueError("format string must be passed by formats")
        if formats:
            if not isinstance(formats, dict):
                raise ValueError("formats must be a level to format string dictionary")
            self.formatters = {}
            for loglevel in formats:
                self.formatters[loglevel] = self.default_formatter(fmt=formats[loglevel], **kwargs)
        else:
            self.formatters = {
                logging.NOTSET: self.default_formatter(fmt=self.default_notset_format, **kwargs),
                logging.DEBUG: self.default_formatter(fmt=self.default_debug_format, **kwargs),
                logging.INFO: self.default_formatter(fmt=self.default_info_format, **kwargs),
                logging.WARNING: self.default_formatter(fmt=self.default_warning_format, **kwargs),
                logging.ERROR: self.default_formatter(fmt=self.default_error_format, **kwargs),
                logging.CRITICAL: self.default_formatter(fmt=self.default_critical_format, **kwargs),
            }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self.formatters.get(record.levelno, self.formatters.get(logging.NOTSET))
        return formatter.format(record)


class _InlineFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def format(self, record: logging.LogRecord) -> str:
        time = datetime.datetime.fromtimestamp(record.created, datetime.datetime.now().astimezone().tzinfo).strftime(
            _JsonFormatter.default_time_format
        )
        keyword: dict[str, Any] = dict()
        record_tags = getattr(record, "tags", None)
        if record_tags and isinstance(record_tags, dict):
            keyword |= record_tags
        record_vars = getattr(record, "vars", None)
        if record_vars and isinstance(record_vars, dict):
            keyword |= record_vars
        if record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            keyword["caller"] = f"{record.module}:{record.lineno}"
        if keyword:
            if record.exc_info:
                return f"{time} {record.levelname[0]} | {record.msg} | {json.dumps(keyword)}\n{self.formatException(record.exc_info)}"
            else:
                return f"{time} {record.levelname[0]} | {record.msg} | {json.dumps(keyword)}"
        else:
            if record.exc_info:
                return f"{time} {record.levelname[0]} | {record.msg}\n{self.formatException(record.exc_info)}"
            else:
                return f"{time} {record.levelname[0]} | {record.msg}"


class _JsonFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def __init__(self, indent=None, **kwargs):
        self._indent = indent

    def format(self, record: logging.LogRecord) -> str:
        keyword: dict[str, Any] = dict()
        record_tags = getattr(record, "tags", None)
        if record_tags and isinstance(record_tags, dict):
            keyword |= record_tags
        record_vars = getattr(record, "vars", None)
        if record_vars and isinstance(record_vars, dict):
            keyword |= record_vars
        json_record = dict()
        json_record["message"] = record.msg
        json_record["level"] = record.levelname
        json_record["time"] = datetime.datetime.fromtimestamp(
            record.created, datetime.datetime.now().astimezone().tzinfo
        ).strftime(_JsonFormatter.default_time_format)
        json_record["server"] = socket.gethostname()
        if keyword:
            json_record["keyword"] = keyword
        if record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            json_record["caller"] = f"{record.module}:{record.lineno}"
        if record.exc_info:
            json_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(json_record, indent=self._indent)
