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

import pytest
from gulper.module import Config, get_config


def test_config():
    """Config Tests"""
    config = get_config("config.example.yaml")

    assert (
        config.get_storages().get("aws_s3_01").get("access_key_id")
        == "your_access_key_id"
    )
    assert (
        config.get_storages().get("aws_s3_01").get("secret_access_key")
        == "your_secret_access_key"
    )
    assert config.get_storages().get("aws_s3_01").get("region") == "your_region"
    assert config.get_storages().get("aws_s3_01").get("path") == "/"
    assert config.get_storages().get("aws_s3_01").get("retention") == "1 years"


def test_get_storages():
    config = get_config("config.example.yaml")
    storages = config.get_storages()
    assert isinstance(storages, dict)
    assert "local_01" in storages
    assert "aws_s3_01" in storages
    assert "local_02" in storages


def test_get_schedules():
    config = get_config("config.example.yaml")
    schedules = config.get_schedules()
    assert isinstance(schedules, dict)
    assert "daily_01" in schedules


def test_get_databases():
    config = get_config("config.example.yaml")
    databases = config.get_databases()
    assert isinstance(databases, dict)
    assert "db01" in databases
    assert "db02" in databases
    assert "db03" in databases
    assert "db04" in databases


def test_get_storage_config():
    config = get_config("config.example.yaml")
    storage_config = config.get_storage_config("local_01")
    assert isinstance(storage_config, dict)
    assert "path" in storage_config
    assert "retention" in storage_config

    # Test non-existent storage
    non_existent_config = config.get_storage_config("non_existent")
    assert non_existent_config is None


def test_get_schedule_config():
    config = get_config("config.example.yaml")
    schedule_config = config.get_schedule_config("daily_01")
    assert isinstance(schedule_config, dict)
    assert "expression" in schedule_config

    # Test non-existent schedule
    non_existent_config = config.get_schedule_config("non_existent")
    assert non_existent_config is None


def test_get_database_config():
    config = get_config("config.example.yaml")
    database_config = config.get_database_config("db01")
    assert isinstance(database_config, dict)
    assert "type" in database_config
    assert "host" in database_config
    assert "username" in database_config
    assert "password" in database_config
    assert "database" in database_config
    assert "storage" in database_config
    assert "schedule" in database_config
    assert "options" in database_config

    # Test non-existent database
    non_existent_config = config.get_database_config("non_existent")
    assert non_existent_config is None


def test_parse_retention():
    config = get_config("config.example.yaml")
    assert config._parse_retention("30 days") == 30
    assert config._parse_retention("1 months") == 30
    assert config._parse_retention("1 years") == 365

    with pytest.raises(ValueError):
        config._parse_retention("invalid format")

    with pytest.raises(ValueError):
        config._parse_retention("30 invalid_unit")


def test_get_retention_in_days():
    config = get_config("config.example.yaml")
    retention_days = config.get_retention_in_days("local_01")
    assert retention_days == 90  # 3 months

    retention_days = config.get_retention_in_days("aws_s3_01")
    assert retention_days == 365  # 1 year

    retention_days = config.get_retention_in_days("local_02")
    assert retention_days == 20  # 20 days

    # Test non-existent storage
    non_existent_retention = config.get_retention_in_days("non_existent")
    assert non_existent_retention is None


def test_get_config():
    config = get_config("config.example.yaml")
    assert isinstance(config, Config)
    assert isinstance(config.config, dict)
