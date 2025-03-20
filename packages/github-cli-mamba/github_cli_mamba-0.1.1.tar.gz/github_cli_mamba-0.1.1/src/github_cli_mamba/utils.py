import csv
import json
import sys
from typing import List

import jmespath
from rich import print, print_json
from rich.console import Console
from rich.table import Table

from github_cli_mamba.options import OutputOption


def print_beautify(data: List[dict], output_option: OutputOption):
    if output_option == OutputOption.json:
        # json key is double quotes, python dict key is single quotes
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        print_json(json.dumps(data))
    elif output_option == OutputOption.csv:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    elif output_option == OutputOption.table:
        table = Table()
        table.add_column("")
        for field in data[0].keys():
            table.add_column(str(field))
        for row in data:
            table.add_row(*[str(data.index(row) + 1)] + [str(v) for v in row.values()])
        console = Console()
        console.print(table)


def sort_by_field(data: List[dict], field_list: List[str], reverse: bool = False):
    field_list.reverse()

    expr = ""
    for field in field_list:
        if expr:
            expr = f"sort_by(@, &{field})"
        else:
            expr = f"sort_by({expr}, &{field})"

    if reverse:
        expr = f"{expr}.reverse(@)"

    return jmespath.search(expr, data)
