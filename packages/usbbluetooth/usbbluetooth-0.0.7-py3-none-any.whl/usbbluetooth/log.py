#!/usr/bin/env python

from enum import IntEnum


class LogLevel(IntEnum):
    NONE = 0
    ERROR = 1,
    WARN = 2,
    INFO = 3,
    DEBUG = 4
