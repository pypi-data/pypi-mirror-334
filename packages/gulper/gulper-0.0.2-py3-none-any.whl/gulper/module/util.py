# MIT License
#
# Copyright (c) 2025 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Dict, Any
from rich.table import Table
from rich import print
from rich.console import Console
from rich.markdown import Markdown


def message(message: str):
    """
    Print a message

    Args:
        message (str): The message to show
    """
    print(f"[bold green]{message}[/bold green]")


def success(message: str):
    """
    Print a success message with green formatting.

    Args:
        message (str): The success message to be printed.
    """
    print(f"[bold green][SUCCESS][/bold green] {message}")
    exit(0)


def error(message: str):
    """
    Print an error message with red formatting.

    Args:
        message (str): The error message to be printed.
    """
    print(f"[bold red][ERROR][/bold red] {message}")
    exit(1)


def backups_table(data: list[Dict[str, Any]]):
    """
    Print a tabular data

    Args:
        data (list[Dict[str, Any]]): The data to output
    """
    # Create a console object
    console = Console()

    # Create a table
    table = Table(title="Database Backups")

    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Database Name", style="magenta")
    table.add_column("Status", justify="center", style="green")
    table.add_column("Created At (UTC)", style="yellow")
    table.add_column("Updated At (UTC)", style="yellow")

    # Add rows to the table
    for item in data:
        table.add_row(
            item["id"],
            item["db"],
            item["status"].title(),
            item["createdAt"],
            item["updatedAt"],
        )

    console.print(table)
    exit(0)


def logs_table(data: list[Dict[str, Any]]):
    """
    Print a tabular data

    Args:
        data (list[Dict[str, Any]]): The data to output
    """
    print(data)
    exit(0)


def backup_info(backup):
    backup["status"] = backup["status"].title()

    markdown = f"""- **Backup ID**: {backup.get("id")}
- **Database**:  {backup.get("db")}
- **Status**:  {backup.get("status")}
- **Backups Exists**: {backup.get("backups_exists")}
- **Created At**:  {backup.get("createdAt")}
- **Updated At**:  {backup.get("updatedAt")}
"""

    for file in backup["meta"]["backups"]:
        markdown += f"- **{file.get('storage_name')}**: {file.get('file')}\n"

    console = Console()
    md = Markdown(markdown)
    console.print(md)
    exit(0)
