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

import yaml
from typing import Dict, Any, Optional


class Config:
    """Config Class"""

    def __init__(self, config_file: str) -> None:
        """
        Initialize the Config object and load the configuration from a YAML file.

        Args:
            config_file (str): Path to the YAML configuration file.
        """
        self.config = self._load_config(config_file)

    def _load_config(self, file_path: str) -> Dict[str, Any]:
        """
        Load the configuration from a YAML file.

        Args:
            file_path (str): Path to the YAML configuration file.

        Returns:
            Dict[str, Any]: Parsed configuration data.
        """
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def get_temp_dir(self) -> str:
        """
        Get temp dir path

        Returns:
            str: The temp dir path
        """
        return self.config.get("temp_dir", "/tmp").rstrip("/")

    def get_state_file(self) -> str:
        """
        Get state file path

        Returns:
            str: The state file path
        """
        return self.config.get("state_file", "/tmp/gulper.db")

    def get_logging_level(self) -> str:
        """
        Get logging level

        Returns:
            str: the logging level
        """
        return self.config.get("logging").get("level", "error")

    def get_logging_handler(self) -> str:
        """
        Get logging handler

        Returns:
            str: the logging handler
        """
        return self.config.get("logging").get("handler", "console")

    def get_logging_path(self) -> str:
        """
        Get logging path

        Returns:
            str: the logging path
        """
        return self.config.get("logging").get("path", "~")

    def get_storages(self) -> Dict[str, Any]:
        """
        Get all storage configurations.

        Returns:
            Dict[str, Any]: Dictionary of storage configurations.
        """
        return self.config.get("storage", {})

    def get_schedules(self) -> Dict[str, Any]:
        """
        Get all schedule configurations.

        Returns:
            Dict[str, Any]: Dictionary of schedule configurations.
        """
        return self.config.get("schedule", {})

    def get_databases(self) -> Dict[str, Any]:
        """
        Get all database configurations.

        Returns:
            Dict[str, Any]: Dictionary of database configurations.
        """
        return self.config.get("database", {})

    def get_storage_config(self, storage_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the configuration for a specific storage by name.

        Args:
            storage_name (str): Name of the storage configuration to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Storage configuration if found; otherwise None.
        """
        return self.config.get("storage").get(storage_name, None)

    def get_schedule_config(self, schedule_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the configuration for a specific schedule by name.

        Args:
            schedule_name (str): Name of the schedule configuration to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Schedule configuration if found; otherwise None.
        """
        return self.config.get("schedule").get(schedule_name, None)

    def get_database_config(self, database_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the configuration for a specific database by name.

        Args:
            database_name (str): Name of the database configuration to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Database configuration if found; otherwise None.
        """
        return self.config.get("database").get(database_name, None)

    def _parse_retention(self, retention_str: str) -> int:
        """
        Parse retention string into days.

        Args:
            retention_str (str): Retention period (e.g., "3 months", "20 days", "1 year").

        Returns:
            int: Retention period in days.

        Raises:
            ValueError: If the unit is unsupported.
        """
        parts = retention_str.split()

        if len(parts) != 2:
            raise ValueError(
                "Invalid retention format. Expected format is '<value> <unit>'."
            )

        value = int(parts[0])
        unit = parts[1]

        if unit == "days" or unit == "day":
            return value
        elif unit == "months" or unit == "month":
            return value * 30
        elif unit == "years" or unit == "year":
            return value * 365
        else:
            raise ValueError("Unsupported unit for retention period.")

    def get_retention_in_days(self, db_name: str) -> Optional[int]:
        """
        Get the retention period in days for a specific storage.

        Args:
            db_name (str): name of the database.

        Returns:
            Optional[int]: Retention period in days if found; otherwise None.
        """
        db_config = self.get_database_config(db_name)

        if db_config and "retention" in db_config:
            return self._parse_retention(db_config["retention"])

        return None


def get_config(config_file: str) -> Config:
    """
    Create and return a Config object from a specified configuration file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        Config: A Config object initialized with the provided configuration file.
    """
    return Config(config_file)
