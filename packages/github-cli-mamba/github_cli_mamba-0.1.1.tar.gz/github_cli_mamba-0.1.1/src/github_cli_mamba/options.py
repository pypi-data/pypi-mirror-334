from enum import Enum


class OutputOption(str, Enum):
    json = "json"
    table = "table"
    csv = "csv"
