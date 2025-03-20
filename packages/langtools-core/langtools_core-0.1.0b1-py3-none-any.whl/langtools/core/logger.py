import logging
import platform
import socket
import sys
from typing import Optional, Any
from logging import LogRecord, Handler, Formatter as BaseFormatter
from datetime import datetime, timezone
from .exporters.console_exporter import ConsoleLogHandler
from .exporters.file_exporter import FileLogHandler
from .exporters.azure_monitor import AzureMonitorSDKLogHandler
import orjson, copy

sdklogger_name = "sdk-logger"

class ExtendedLogRecord(LogRecord):
    """An extended LogRecord with additional system and metadata attributes."""
    
    def __init__(self, name: str, level: int, pathname: str, lineno: int,
                 msg: str, args: Any, exc_info: Any, func: Optional[str] = None,
                 sinfo: Optional[str] = None, **kwargs):
        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo)
        
        # Add extended attributes
        self.nodeArch = platform.architecture()[0]
        self.os = platform.system()
        self.platformversion = platform.version()
        self.runtimeversion = f'Python {sys.version.split()[0]}'
        self.SDKversion = self.getSDKVersion()
        self.machineName = platform.node()
        
        # Get IP address
        try:
            self.IP = socket.gethostbyname(socket.gethostname())
        except:
            self.IP = 'unknown'


    def getSDKVersion(self):
        try:
             import importlib.metadata
             sdkname = 'langtools-core'
             return f'{sdkname}-{importlib.metadata.version(sdkname)}'
        except:
            # Fallback to a default version if importlib.metadata is not available
            return 'unknown'

class Formatter(BaseFormatter):
    """Formatter for logs following the specification format."""
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(
            fmt or '%(timestamp)s - %(name)s - %(levelname)s - %(message)s - %(IP)s - %(machineName)s',
            datefmt)
    
    def format(self, record):
        # Convert to UTC time
        record.timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime("%m-%d-%Y %H:%M:%S")
        # Process extra attributes, serializing dictionaries
        if not hasattr(record, 'metadata'):
            record.metadata = ''
        return super().format(record)

class Logger(logging.Logger):
    """Logger class that follows the langtools core specification."""
    
    _formatter = None
    _handlers = None
    _level = None
    
    # Standard logging levels
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    def __init__(self, name: str):
        """Initialize a new logger instance."""
        super().__init__(name)

    @classmethod
    def basicConfig(cls, format: str = '%(timestamp)s - %(name)s - %(levelname)s - %(message)s',
                   level: int = INFO, handlers: list = None) -> None:
        """
        Configure the logging system with specified format, level, and handlers.
        
        Args:
            format: The format string for the handler
            level: The root logger level
            handlers: List of handlers to add to the root logger
        """
        cls._handlers = handlers or [ConsoleLogHandler()]

        # Initialize formatter
        cls._formatter = Formatter(format)
            
        cls._level = level
        
        # Configure handlers
        for handler in cls._handlers:
            if not handler.formatter:
                handler.setFormatter(cls._formatter)
            if not handler.level:
                handler.setLevel(cls._level)

        logging.basicConfig(level=cls._level, handlers=cls._handlers)
        logging.setLogRecordFactory(ExtendedLogRecord)

    @classmethod
    def getLogger(cls, name: Optional[str] = None) -> 'Logger':
        """
        Return a logger with the specified name.
        
        Args:
            name: The logger name. If None, return the root logger.
        """
        if cls._handlers is None:
            Logger.basicConfig()
        logger = logging.getLogger(name)
        if logger.handlers is None or logger.handlers == []:
            logger.handlers = copy.copy(cls._handlers)
        logger.propagate = False
        return logger
    
    def addHandler(cls, hdlr: Handler) -> None:
        """Add the specified handler to this logger."""
        if cls._formatter and not hdlr.formatter:
            hdlr.setFormatter(cls._formatter)
        super().addHandler(hdlr)

class SDKLogger:

    _sdklogger = None

    @classmethod
    def initSdklogger(cls, enable_sdk_logger: bool = True, level: int = Logger.DEBUG, format: str = '%(message)s') -> None:
        """
        Init a logger with name 'sdk-logger', configure AzureMonitorSDKLogHandler.
    
        Args:
            enable_sdk_logger: Whether to enable sdk logger
            level: The logging level to use
    
        Returns:
            logging.Logger: A logger instance with name 'sdk-logger'
        """
        if cls._sdklogger is not None:
            cls._sdklogger.warning("Don't override existing sdk-logger.")
            return
        cls._sdklogger = Logger.getLogger(sdklogger_name)
        # Clear all existing handlers in sdk-logger
        for handler in cls._sdklogger.handlers[:]:
            cls._sdklogger.removeHandler(handler)
        cls._sdklogger.propagate = False
        handler = AzureMonitorSDKLogHandler(enable_sdk_logger, level)
        handler.setFormatter(Formatter(format))
        cls._sdklogger.addHandler(handler)

    @classmethod
    def getSdklogger(cls) -> Logger:
        """
        Get the SDK logger instance, initializing it if necessary.
    
        Returns:
            Logger: The SDK logger instance
        """
        if cls._sdklogger is None:
            cls.initSdklogger()
        return cls._sdklogger
    
    @classmethod
    def resetLogger(cls) -> None:
        """
        Reset the SDK logger by removing all handlers and cleaning up resources.
        This method should be called when you want to completely reset the logger state.
        """
        if cls._sdklogger is not None:
            # Remove and close all handlers
            for handler in cls._sdklogger.handlers[:]:
                # Flush and close the handler
                handler.flush()
                handler.close()
                cls._sdklogger.removeHandler(handler)
            
            # Reset the logger
            cls._sdklogger.propagate = False
            cls._sdklogger = None