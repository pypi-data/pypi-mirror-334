from logging import LogRecord
from typing import Sequence
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.trace import Span
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.metrics.export import (
    MetricExporter,
    MetricExportResult
)


class NoOpLogHandler(LoggingHandler):
    """A no-op log handler that does nothing with log records."""

    def __init__(self):
        """Initialize the no-op log handler."""
        logger_provider = LoggerProvider()
        super().__init__(logger_provider=logger_provider)

    def emit(self, record: LogRecord) -> None:
        """Do nothing with the log record."""
        pass


class NoOpTraceExporter(SpanExporter):
    """A no-op trace exporter that does nothing with spans."""

    def export(self, spans: Sequence[Span]) -> SpanExportResult:
        """Do nothing and return success."""
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        """Do nothing for shutdown."""
        pass

    def force_flush(self, timeout_millis: float = 30000) -> bool:
        """Do nothing and return success."""
        return True


class NoOpMetricExporter(MetricExporter):
    """A no-op metric exporter that does nothing with metrics."""

    def __init__(self):
        """Initialize the no-op metric exporter."""
        super().__init__()

    def export(self, metrics_data, timeout_millis: float = 10000) -> MetricExportResult:
        """Do nothing and return success."""
        return MetricExportResult.SUCCESS

    def force_flush(self, timeout_millis: float = 10000) -> bool:
        """Do nothing and return success."""
        return True

    def shutdown(self, timeout_millis: float = 30000, **kwargs) -> None:
        """Do nothing for shutdown."""
        self._is_shutdown = True


__all__ = ['NoOpLogHandler', 'NoOpTraceExporter', 'NoOpMeterExporter']