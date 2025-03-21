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

from typing import Optional
from gulper.core import Log
from gulper.module import Output


class LogCommand:
    """
    Log Command
    """

    def __init__(self, log: Log, output: Output):
        """
        Class Constructor

        Args:
            log (Log): The log class instance
            output (Output): output class instance
        """
        self._log = log
        self._output = output
        self._log.setup()

    def list(self, db_name: Optional[str], since: Optional[str], as_json: bool):
        """
        Output a list of logs

        Args:
            db_name (str): The database name
            since (str): A certain period for the backup
            as_json (bool): whether to output as JSON
        """
        try:
            logs = self._log.list(db_name, since)
        except Exception as e:
            self._output.error_message(str(e), as_json)

        self._output.show_logs(logs, as_json)


def get_log_command(log: Log, output: Output) -> LogCommand:
    """
    Get an instance of log command

    Args:
        log (Log): An instance of log class
        output (Output): output class instance

    Returns:
        LogCommand: an instance of log command
    """
    return LogCommand(log, output)
