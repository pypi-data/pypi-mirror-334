import asyncio
from enum import Enum, auto
import datetime
import aiofiles
import aiofiles.os
import logging
import os
import sys
from typing import Optional, Dict, Any, List, Union

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    NOTICE = auto()
    ERROR = auto()
    CRITICAL = auto()
    OKAY = auto()

    @classmethod
    def from_string(cls, level_str: str) -> 'LogLevel':
        try:
            return cls[level_str.upper()]
        except KeyError:
            return cls.INFO

class ConsoleHandler:
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors and sys.stdout.isatty()
        self.colors = {
            LogLevel.DEBUG: '\033[94m',
            LogLevel.INFO: '\033[97m',
            LogLevel.WARNING: '\033[93m',
            LogLevel.ERROR: '\033[91m',
            LogLevel.CRITICAL: '\033[41m\033[97m',
            LogLevel.OKAY: '\033[92m',
            LogLevel.NOTICE: '\033[96m',
        }
        self.reset = '\033[0m'

    async def handle(self, log_entry: str, level: LogLevel):
        color = self.colors.get(level, '') if self.use_colors else ''
        print(f"{color}{log_entry}{self.reset if color else ''}")

class FileHandler:
    def __init__(self, 
                 filename: str, 
                 max_size: int = 1024*1024, 
                 backup_count: int = 5,
                 encoding: str = 'utf-8'):
        self.filename = filename
        self.max_size = max_size
        self.backup_count = backup_count
        self.encoding = encoding
        # self._ensure_directory()

    async def _ensure_directory(self):
        dir_path = os.path.dirname(self.filename)
        try:
            await aiofiles.os.makedirs(dir_path, exist_ok=True)
        except Exception as e:
            logging.error(f"Error creating directory {dir_path}: {e}")

    async def _create_file_if_not_exists(self):
        try:
            if not await aiofiles.os.path.exists(self.filename):
                async with aiofiles.open(self.filename, 'w') as f:
                    await f.write('')
        except Exception as e:
            logging.error(f"Error creating file {self.filename}: {e}")
            
    async def _rotate(self):
        await self._ensure_directory()
        await self._create_file_if_not_exists()
        
        if await aiofiles.os.path.getsize(self.filename) < self.max_size:
            return

        for i in range(self.backup_count-1, 0, -1):
            src = f"{self.filename}.{i}"
            dst = f"{self.filename}.{i+1}"
            if await aiofiles.os.path.exists(src):
                await aiofiles.os.rename(src, dst)
        
        if await aiofiles.os.path.exists(self.filename):
            await aiofiles.os.rename(self.filename, f"{self.filename}.1")

    async def handle(self, log_entry: str):
        await self._rotate()
        async with aiofiles.open(self.filename, mode='a', encoding=self.encoding) as f:
            await f.write(log_entry + "\n")

class Metalog:
    def __init__(self, 
                 handlers: Optional[List[Union[ConsoleHandler, FileHandler]]] = None,
                 level: Union[LogLevel, str] = LogLevel.INFO,
                 format_str: str = "{time} | {level:8} | {module}:{funcName}:{lineno} | {message}",
                 extra_fields: Optional[Dict[str, Any]] = None):
        
        self.handlers = handlers or [ConsoleHandler()]
        self.level = level if isinstance(level, LogLevel) else LogLevel.from_string(level)
        self.format_str = format_str
        self.extra_fields = extra_fields or {}
        self.filters = []

    def add_filter(self, filter_func):
        self.filters.append(filter_func)

    async def _should_log(self, level: LogLevel, metadata: dict) -> bool:
        if level.value < self.level.value:
            return False
        
        for filter_func in self.filters:
            if not filter_func(level, metadata):
                return False
        
        return True

    async def _log(self, 
                 level: LogLevel, 
                 message: str,
                 **additional_fields):
        try:
            frame = sys._getframe(2)
            module = frame.f_globals['__name__']
            func_name = frame.f_code.co_name
            lineno = frame.f_lineno
        except:
            module = func_name = lineno = "UNKNOWN"

        metadata = {
            "time": datetime.datetime.now().isoformat(sep=' ', timespec='seconds'),
            "level": level.name,
            "message": message,
            "module": module,
            "funcName": func_name,
            "lineno": lineno,
            **self.extra_fields,
            **additional_fields
        }

        if not await self._should_log(level, metadata):
            return

        log_entry = self.format_str.format(**metadata)

        for handler in self.handlers:
            try:
                if isinstance(handler, ConsoleHandler):
                    await handler.handle(log_entry, level)
                else:
                    await handler.handle(log_entry)
            except Exception as e:
                logging.error(f"Error in log handler: {e}")

    def __getattr__(self, name):
        level = name.upper()
        if level in LogLevel.__members__:
            return lambda msg, **kwargs: self._log(LogLevel[level], msg, **kwargs)
        raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")

class AsyncLogHandler(logging.Handler):
    def __init__(self, metalog: Metalog):
        super().__init__()
        self.metalog = metalog
        self.loop = asyncio.get_event_loop()
        self.level_map = {
            logging.DEBUG: LogLevel.DEBUG,
            logging.INFO: LogLevel.INFO,
            logging.WARNING: LogLevel.WARNING,
            logging.ERROR: LogLevel.ERROR,
            logging.CRITICAL: LogLevel.CRITICAL
        }

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        log_level = self.level_map.get(record.levelno, LogLevel.INFO)
        
        asyncio.run_coroutine_threadsafe(
            self.metalog._log(
                log_level,
                message,
                module=record.module,
                funcName=record.funcName,
                lineno=record.lineno
            ),
            self.loop
        )


__all__ = ['LogLevel', 'ConsoleHandler', 'FileHandler', 'Metalog', 'AsyncLogHandler']