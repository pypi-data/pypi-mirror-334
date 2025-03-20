#!/usr/bin/env python
# -*- coding: utf-8 -*-

# パッケージとして実行するための補助
if __name__ == '__main__' and __package__ is None:
    __package__ = "logflex.tests"

import os
import time
import logging
import pathlib
import pytest

from ..config.settings import ConfigLoader, ConfigBuilder
from ..config.watcher import ConfigFileChangeHandler
from ..logflex import CustomLogger
from ..models.config_model import Configuration, GeneralSettings, ColorSettings

# ---------------------------
# テスト1: TOMLファイルからの読み込み
# ---------------------------
def test_configloader_from_file(tmp_path):
    config_toml = """
[general]
log_level = "DEBUG"
verbose = true
trace = false
format = "[%(asctime)s] %(message)s"
enable_dynamic_reloading = false

[general.color_settings]
enable_color = true
datefmt = "%Y-%m-%d"
reset = true
log_colors = { DEBUG = "cyan", INFO = "green", WARNING = "yellow", ERROR = "red", CRITICAL = "red,bg_white" }
style = "%"

[file_handler]
logdir = "tmp_log"
logfile = "app.log"
when = "midnight"
interval = 1
backup_count = 7
dedicate_error_logfile = false

[syslog_handler]
use_syslog = false
syslog_address = "localhost"
syslog_port = 514
syslog_facility = "LOG_USER"
"""
    config_file = tmp_path / "config.toml"
    config_file.write_text(config_toml)
    
    loader = ConfigLoader(config_path=str(config_file))
    config = loader.config

    assert config.general.log_level == "DEBUG"
    assert config.general.verbose is True
    assert config.general.trace is False
    assert config.general.format == "[%(asctime)s] %(message)s"
    assert config.general.enable_dynamic_reloading is False
    assert config.general.color_settings.enable_color is True
    assert config.general.color_settings.datefmt == "%Y-%m-%d"
    assert config.file_handler.logdir == "tmp_log"
    assert config.syslog_handler.use_syslog is False

# ---------------------------
# テスト2: 環境変数からの設定読み込み
# ---------------------------
def test_configloader_from_env(tmp_path, monkeypatch):
    # GeneralSettings.env_keys を上書きして enable_dynamic_reloading キーが文字列を返すようにする
    monkeypatch.setattr(GeneralSettings, "env_keys", lambda: {
        'log_level': 'GENERAL_LOG_LEVEL',
        'verbose': 'GENERAL_VERBOSE',
        'trace': 'GENERAL_TRACE',
        'format': 'GENERAL_FORMAT',
        'color_settings': ColorSettings.env_keys(),
        'enable_dynamic_reloading': 'GENERAL_ENABLE_DYNAMIC_RELOADING'
    })
    monkeypatch.setenv("GENERAL_ENABLE_DYNAMIC_RELOADING", "false")

    # os.getenv を再帰的に処理するようにパッチ
    original_getenv = os.getenv
    def recursive_getenv(key, default=None):
        if isinstance(key, dict):
            return {k: recursive_getenv(v, default) for k, v in key.items()}
        return original_getenv(key, default)
    monkeypatch.setattr(os, "getenv", recursive_getenv)

    non_existent = tmp_path / "nonexistent.toml"
    # general の環境変数設定
    monkeypatch.setenv("GENERAL_LOG_LEVEL", "INFO")
    monkeypatch.setenv("GENERAL_VERBOSE", "true")
    monkeypatch.setenv("GENERAL_TRACE", "false")
    monkeypatch.setenv("GENERAL_FORMAT", "[%(asctime)s] [%(levelname)s]: %(message)s")

    # color_settings 用の環境変数
    monkeypatch.setenv("COLOR_ENABLE_COLOR", "false")
    monkeypatch.setenv("COLOR_DATEFMT", "%H:%M:%S")
    monkeypatch.setenv("COLOR_RESET", "true")
    monkeypatch.setenv("COLOR_LOG_COLORS_DEBUG", "blue")
    monkeypatch.setenv("COLOR_LOG_COLORS_INFO", "white")
    monkeypatch.setenv("COLOR_LOG_COLORS_WARNING", "magenta")
    monkeypatch.setenv("COLOR_LOG_COLORS_ERROR", "red")
    monkeypatch.setenv("COLOR_LOG_COLORS_CRITICAL", "red,bg_white")
    monkeypatch.setenv("COLOR_STYLE", "%")

    # file_handler 用の環境変数
    monkeypatch.setenv("FILEHANDLER_LOGDIR", "env_log")
    monkeypatch.setenv("FILEHANDLER_LOGFILE", "env_app.log")
    monkeypatch.setenv("FILEHANDLER_WHEN", "midnight")
    monkeypatch.setenv("FILEHANDLER_INTERVAL", "1")
    monkeypatch.setenv("FILEHANDLER_BACKUP_COUNT", "7")
    monkeypatch.setenv("FILEHANDLER_DEDICATE_ERROR_LOGFILE", "false")

    # syslog_handler 用の環境変数
    monkeypatch.setenv("SYSLOGHANDLER_USE_SYSLOG", "false")
    monkeypatch.setenv("SYSLOGHANDLER_SYSLOG_ADDRESS", "localhost")
    monkeypatch.setenv("SYSLOGHANDLER_SYSLOG_PORT", "514")
    monkeypatch.setenv("SYSLOGHANDLER_SYSLOG_FACILITY", "LOG_USER")

    loader = ConfigLoader(config_path=str(non_existent))
    config = loader.config

    assert config.general.log_level == "INFO"
    assert config.general.verbose is True
    assert config.general.trace is False
    assert config.general.format == "[%(asctime)s] [%(levelname)s]: %(message)s"
    assert config.general.color_settings.enable_color is False
    assert config.general.color_settings.datefmt == "%H:%M:%S"
    assert config.file_handler.logdir == "env_log"
    assert config.syslog_handler.use_syslog is False

# ---------------------------
# テスト3: ConfigBuilder での設定生成
# ---------------------------
def test_configbuilder_build_config(monkeypatch):
    # 環境変数の影響を除去
    monkeypatch.delenv("GENERAL_LOG_LEVEL", raising=False)
    monkeypatch.delenv("GENERAL_VERBOSE", raising=False)
    monkeypatch.delenv("GENERAL_TRACE", raising=False)
    monkeypatch.delenv("GENERAL_FORMAT", raising=False)
    monkeypatch.delenv("GENERAL_ENABLE_DYNAMIC_RELOADING", raising=False)

    kwargs = {
        "log_level": "WARNING",
        "verbose": True,
        "trace": True,
        "format": "[%(asctime)s] %(message)s",
        "enable_dynamic_reloading": True,
        "color_enable": False,
        "color_datefmt": "%H:%M",
        "color_reset": False,
        "color_log_colors": {
            "DEBUG": "blue",
            "INFO": "white",
            "WARNING": "magenta",
            "ERROR": "red",
            "CRITICAL": "red,bg_white"
        },
        "color_style": "#",
        "file_logdir": "builder_log",
        "file_logfile": "builder.log",
        "file_when": "D",
        "file_interval": 2,
        "file_backup_count": 3,
        "file_dedicate_error_logfile": True,
        "use_syslog": True,
        "syslog_address": "192.168.1.1",
        "syslog_port": 10514,
        "syslog_facility": "LOG_DAEMON"
    }
    config = ConfigBuilder.build_config(**kwargs)

    # kwargs の値が優先されることを確認
    assert config.general.log_level == "WARNING"
    assert config.general.verbose is True
    assert config.general.trace is True
    assert config.general.format == "[%(asctime)s] %(message)s"
    assert config.general.enable_dynamic_reloading is True
    assert config.general.color_settings.enable_color is False
    assert config.general.color_settings.datefmt == "%H:%M"
    assert config.general.color_settings.reset is False
    assert config.general.color_settings.log_colors["DEBUG"] == "blue"
    assert config.file_handler.logdir == "builder_log"
    assert config.file_handler.when == "D"
    assert config.file_handler.interval == 2
    assert config.file_handler.backup_count == 3
    assert config.file_handler.dedicate_error_logfile is True
    assert config.syslog_handler.use_syslog is True
    assert config.syslog_handler.syslog_address == "192.168.1.1"
    assert config.syslog_handler.syslog_port == 10514
    assert config.syslog_handler.syslog_facility == "LOG_DAEMON"

# ---------------------------
# テスト4: CustomLogger の生成および再設定の確認
# ---------------------------
def test_customlogger_creation_and_reconfiguration(tmp_path, monkeypatch):
    # 環境変数の影響を除去
    monkeypatch.delenv("GENERAL_LOG_LEVEL", raising=False)
    monkeypatch.delenv("GENERAL_VERBOSE", raising=False)
    monkeypatch.delenv("GENERAL_TRACE", raising=False)
    monkeypatch.delenv("GENERAL_FORMAT", raising=False)
    monkeypatch.delenv("GENERAL_ENABLE_DYNAMIC_RELOADING", raising=False)

    # 既存の "test_logger" があれば削除（新規生成のため）
    logger_name = "test_logger"
    if logger_name in logging.root.manager.loggerDict:
        del logging.root.manager.loggerDict[logger_name]

    kwargs = {
        "log_level": "DEBUG",
        "verbose": True,
        "trace": False,
        "format": "[%(asctime)s] %(message)s",
        "enable_dynamic_reloading": False,
        "color_enable": False,
        "color_datefmt": "%Y-%m-%d %H:%M:%S",
        "color_reset": True,
        "color_log_colors": {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white"
        },
        "color_style": "%",
        "file_logdir": str(tmp_path / "logs"),
        "file_logfile": "test.log",
        "file_when": "midnight",
        "file_interval": 1,
        "file_backup_count": 5,
        "file_dedicate_error_logfile": False,
        "use_syslog": False,
        "syslog_address": "localhost",
        "syslog_port": 514,
        "syslog_facility": "LOG_USER"
    }
    config = ConfigBuilder.build_config(**kwargs)
    logger = CustomLogger("test_logger", **kwargs)
    # CustomLogger 内で logger.handlers が設定されるはず
    assert logger.level == logging.getLevelName("DEBUG") or logger.level == 10
    assert len(logger.handlers) > 0

    new_kwargs = kwargs.copy()
    new_kwargs["log_level"] = "ERROR"
    new_config = ConfigBuilder.build_config(**new_kwargs)
    CustomLogger.reconfigure_logger(logger, new_config)
    assert logger.level == logging.getLevelName("ERROR") or logger.level == 40

# ---------------------------
# テスト5: ConfigFileChangeHandler の debounce 動作確認
# ---------------------------
# Dummyクラスの修正
class DummyConfigLoader:
    def __init__(self, path):
        self.config_path = path
        self.reload_called = False
        # ダミーの設定を生成
        self.config = ConfigBuilder.build_config(
            log_level="DEBUG",
            verbose=False,
            trace=False,
            format="[%(asctime)s] %(message)s",
            enable_dynamic_reloading=False,
            color_enable=False,
            color_datefmt="",
            color_reset=True,
            color_log_colors={"DEBUG": "blue", "INFO": "white", "WARNING": "yellow", "ERROR": "red", "CRITICAL": "red,bg_white"},
            color_style="%",
            file_logdir="",
            file_logfile="",
            file_when="midnight",
            file_interval=1,
            file_backup_count=7,
            file_dedicate_error_logfile=False,
            use_syslog=False,
            syslog_address="localhost",
            syslog_port=514,
            syslog_facility="LOG_USER"
        )

    def reload_config(self):
        self.reload_called = True
        return True

class DummyLogger:
    def __init__(self):
        self.messages = []
        self.handlers = []  # handlers属性を追加
        self.level = None
    def info(self, msg):
        self.messages.append(("info", msg))
    def warning(self, msg):
        self.messages.append(("warning", msg))
    def setLevel(self, level):
        self.level = level
    def addFilter(self, filt):
        pass
    def addHandler(self, handler):
        self.handlers.append(handler)

class DummyEvent:
    def __init__(self, src_path):
        self.src_path = src_path

def test_configfile_change_handler(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text("dummy")
    loader = DummyConfigLoader(config_path)
    dummy_logger = DummyLogger()
    handler = ConfigFileChangeHandler(loader, dummy_logger)
    event = DummyEvent(str(config_path))

    # 初回の変更で reload が実行される
    handler.on_modified(event)
    assert loader.reload_called is True
    info_msgs = [msg for level, msg in dummy_logger.messages if level == "info"]
    assert any("Config file was reloaded" in m for m in info_msgs)

    # 連続呼び出し時は debounce により reload が呼ばれない
    loader.reload_called = False
    handler.last_modified = time.time()  # 現在時刻に設定
    handler.on_modified(event)
    assert loader.reload_called is False
