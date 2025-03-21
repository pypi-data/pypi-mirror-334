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

import json
from typing import Optional
from gulper.module import Config
from gulper.module import State
from gulper.module import Logger
from gulper.module import get_storage
from gulper.module import get_database
from gulper.exception import BackupNotFound
from gulper.exception import OperationFailed


class Restore:
    """
    Restore Core Functionalities
    """

    def __init__(self, config: Config, state: State, logger: Logger):
        """
        Class Constructor

        Args:
            config (Config): A config instance
            state (State): A state instance
            logger (Logger): A logger instance
        """
        self._config = config
        self._state = state
        self._logger = logger

    def setup(self):
        """
        Setup calls
        """
        self._logger.get_logger().info("Connect into the state database")
        self._state.connect()
        self._logger.get_logger().info("Migrate the state database tables")
        self._state.migrate()

    def run(self, db_name: Optional[str], backup_id: Optional[str]) -> bool:
        """
        Restore a database from a backup

        Args:
            db_name (str): The database name
            backup_id (str): The backup id

        Returns:
            bool: whether the restore succeeded or not
        """
        if db_name:
            backup = self._state.get_latest_backup(db_name)
        elif backup_id:
            backup = self._state.get_backup_by_id(backup_id)
        else:
            raise Exception("Database name or backup id must be provided")

        if backup is None:
            raise BackupNotFound(f"Backup with id {id} not found!")

        backup_exists = True
        meta = json.loads(backup.get("meta"))

        file = None
        for backup_file in meta["backups"]:
            try:
                storage = get_storage(self._config, backup_file.get("storage_name"))
                local_file = "{}/{}.tar.gz".format(
                    self._config.get_temp_dir(), backup.get("id")
                )
                storage.download_file(backup_file.get("file"), local_file)
                file = backup_file.get("file")
                backup_exists = True
            except Exception as e:
                backup_exists = False
                self._logger.get_logger().error(
                    "Unable to restore backup {} file {} in storage {}: {}".format(
                        backup.get("id"),
                        backup_file.get("file"),
                        backup_file.get("storage_name"),
                        str(e),
                    )
                )
            if backup_exists and file:
                break

        if file is None:
            raise BackupNotFound(f"Backup with id {id} not found!")

        try:
            database = get_database(self._config, backup.get("db"))
            database.restore("{}/{}".format(self._config.get_temp_dir(), file))
            self._state.insert_log(
                {
                    "db": backup.get("db"),
                    "type": "info",
                    "record": f"Backup with id {id} restored successfully",
                }
            )
        except Exception as e:
            self._state.insert_log(
                {
                    "db": backup.get("db"),
                    "type": "error",
                    "record": f"Failed to restore backup with id {id}",
                }
            )
            raise OperationFailed(
                "Failed to restore database {}: {}".format(backup.get("db"), str(e))
            )
        return True


def get_restore(config: Config, state: State, logger: Logger) -> Restore:
    """
    Get Restore Class Instance

    Args:
        config (Config): A config instance
        state (State): A state instance
        logger (Logger): A logger instance

    Returns:
        Restore: An instance of restore class
    """
    return Restore(config, state, logger)
