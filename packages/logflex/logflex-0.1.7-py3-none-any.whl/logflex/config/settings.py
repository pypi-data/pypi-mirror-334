#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import toml
import dacite
from typing import Optional
from logflex.models.config_model import (
    Configuration,
    GeneralSettings,
    FileHandlerSettings,
    SyslogHandlerSettings,
    ColorSettings
)

def str_to_bool(val: str) -> bool:
    return val.lower() in ('true', '1', 't', 'yes', 'y')

class ConfigLoader:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = pathlib.Path(config_path or (os.getcwd() + '/config.toml'))
        self.config = self._load_config()

    def _load_config(self) -> Configuration:
        if self.config_path.exists():
            file_config = self._load_config_from_file()
            return self._merge_env(file_config)
        return self._load_config_from_env()

    def _load_config_from_file(self) -> Configuration:
        raw_config = toml.load(self.config_path)
        return dacite.from_dict(
            data_class=Configuration,
            data=raw_config,
            config=dacite.Config(strict=True)
        )

    def _load_config_from_env(self) -> Configuration:
        def get_env_value(cls, field, default=None):
            key = cls.env_keys().get(field)
            if isinstance(key, dict):
                return {k: os.getenv(v, default) for k, v in key.items()}
            return os.getenv(key, default)

        general_settings = GeneralSettings(
            log_level=get_env_value(GeneralSettings, 'log_level') or "INFO",
            verbose=str_to_bool(get_env_value(GeneralSettings, 'verbose') or "false"),
            trace=str_to_bool(get_env_value(GeneralSettings, 'trace') or "false"),
            format=get_env_value(GeneralSettings, 'format') or "[%(asctime)s] [%(levelname)s][%(module)s]: %(message)s",
            enable_dynamic_reloading=str_to_bool(get_env_value(GeneralSettings, 'enable_dynamic_reloading') or "false"),
            color_settings=ColorSettings(
                enable_color=str_to_bool((get_env_value(GeneralSettings, 'color_settings') or {}).get('enable_color', "false")),
                datefmt=(get_env_value(GeneralSettings, 'color_settings') or {}).get('datefmt'),
                reset=str_to_bool((get_env_value(GeneralSettings, 'color_settings') or {}).get('reset', "true")),
                log_colors=(get_env_value(GeneralSettings, 'color_settings') or {}).get('log_colors'),
                style=(get_env_value(GeneralSettings, 'color_settings') or {}).get('style')
            )
        )

        file_handler_settings = FileHandlerSettings(
            logdir=get_env_value(FileHandlerSettings, 'logdir'),
            logfile=get_env_value(FileHandlerSettings, 'logfile'),
            when=get_env_value(FileHandlerSettings, 'when'),
            interval=int(get_env_value(FileHandlerSettings, 'interval', "1")),
            backup_count=int(get_env_value(FileHandlerSettings, 'backup_count', "7")),
            dedicate_error_logfile=get_env_value(FileHandlerSettings, 'dedicate_error_logfile')
        )

        syslog_handler_settings = SyslogHandlerSettings(
            use_syslog=str_to_bool(get_env_value(SyslogHandlerSettings, 'use_syslog') or "false"),
            syslog_address=get_env_value(SyslogHandlerSettings, 'syslog_address') or "localhost",
            syslog_port=int(get_env_value(SyslogHandlerSettings, 'syslog_port', "514")),
            syslog_facility=get_env_value(SyslogHandlerSettings, 'syslog_facility') or "LOG_USER"
        )

        return Configuration(
            general=general_settings,
            file_handler=file_handler_settings,
            syslog_handler=syslog_handler_settings
        )

    def _merge_env(self, config: Configuration) -> Configuration:
        # GeneralSettings の上書き
        for field, env_key in GeneralSettings.env_keys().items():
            if field == 'color_settings':
                # 各カラー設定項目を処理
                color_keys = ColorSettings.env_keys()
                for c_field, c_env_key in color_keys.items():
                    if isinstance(c_env_key, dict):
                        for sub_field, sub_env_key in c_env_key.items():
                            env_val = os.getenv(sub_env_key)
                            if env_val is not None:
                                if config.general.color_settings.log_colors is None:
                                    config.general.color_settings.log_colors = {}
                                config.general.color_settings.log_colors[sub_field] = env_val
                    else:
                        env_val = os.getenv(c_env_key)
                        if env_val is not None:
                            if c_field in ('enable_color', 'reset'):
                                env_val = str_to_bool(env_val)
                            setattr(config.general.color_settings, c_field, env_val)
            else:
                env_val = os.getenv(env_key)
                if env_val is not None:
                    if field in ('verbose', 'trace', 'enable_dynamic_reloading'):
                        env_val = str_to_bool(env_val)
                    setattr(config.general, field, env_val)
        # FileHandlerSettings の上書き
        for field, env_key in FileHandlerSettings.env_keys().items():
            if isinstance(env_key, dict):
                continue
            env_val = os.getenv(env_key)
            if env_val is not None:
                if field in ('interval', 'backup_count'):
                    try:
                        env_val = int(env_val)
                    except Exception:
                        pass
                setattr(config.file_handler, field, env_val)
        # SyslogHandlerSettings の上書き
        for field, env_key in SyslogHandlerSettings.env_keys().items():
            env_val = os.getenv(env_key)
            if env_val is not None:
                if field in ('syslog_port',):
                    try:
                        env_val = int(env_val)
                    except Exception:
                        pass
                setattr(config.syslog_handler, field, env_val)
        return config

class ConfigBuilder:
    @staticmethod
    def build_config(**kwargs) -> Configuration:
        general_settings = ConfigBuilder._create_general_settings(kwargs)
        file_handler_settings = ConfigBuilder._create_file_handler_settings(kwargs)
        syslog_handler_settings = ConfigBuilder._create_syslog_handler_settings(kwargs)
        return Configuration(
            general=general_settings,
            file_handler=file_handler_settings,
            syslog_handler=syslog_handler_settings
        )

    @staticmethod
    def _create_general_settings(config_kwargs) -> GeneralSettings:
        # 環境変数の値を優先し、かつ文字列の場合は明示的に変換
        log_level = os.environ.get('GENERAL_LOG_LEVEL', config_kwargs.get('log_level', 'INFO'))
        verbose_env = os.environ.get('GENERAL_VERBOSE')
        verbose = str_to_bool(verbose_env) if verbose_env is not None else config_kwargs.get('verbose', False)
        trace_env = os.environ.get('GENERAL_TRACE')
        trace = str_to_bool(trace_env) if trace_env is not None else config_kwargs.get('trace', False)

        return GeneralSettings(
            log_level=log_level,
            verbose=verbose,
            trace=trace,
            format=config_kwargs.get('format', "[%(asctime)s] [%(levelname)s][%(module)s]: %(message)s"),
            enable_dynamic_reloading=str_to_bool(os.environ.get('GENERAL_ENABLE_DYNAMIC_RELOADING', str(config_kwargs.get('enable_dynamic_reloading', False)))),
            color_settings=ColorSettings(
                enable_color=str_to_bool(os.environ.get('COLOR_ENABLE_COLOR', str(config_kwargs.get('color_enable', True)))),
                datefmt=os.environ.get('COLOR_DATEFMT', config_kwargs.get('color_datefmt', None)),
                reset=str_to_bool(os.environ.get('COLOR_RESET', str(config_kwargs.get('color_reset', True)))),
                log_colors=config_kwargs.get('color_log_colors', {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white'
                }),
                secondary_log_colors={},
                style=os.environ.get('COLOR_STYLE', config_kwargs.get('color_style', '%')),
            )
        )

    @staticmethod
    def _create_file_handler_settings(config_kwargs) -> FileHandlerSettings:
        return FileHandlerSettings(
            logdir=config_kwargs.get('file_logdir', None),
            logfile=config_kwargs.get('file_logfile', None),
            when=config_kwargs.get('file_when', 'midnight'),
            interval=config_kwargs.get('file_interval', 1),
            backup_count=config_kwargs.get('file_backup_count', 7),
            dedicate_error_logfile=config_kwargs.get('file_dedicate_error_logfile', None)
        )

    @staticmethod
    def _create_syslog_handler_settings(config_kwargs) -> SyslogHandlerSettings:
        return SyslogHandlerSettings(
            use_syslog=config_kwargs.get('use_syslog', False),
            syslog_address=config_kwargs.get('syslog_address', 'localhost'),
            syslog_port=config_kwargs.get('syslog_port', 514),
            syslog_facility=config_kwargs.get('syslog_facility', 'LOG_USER')
        )
