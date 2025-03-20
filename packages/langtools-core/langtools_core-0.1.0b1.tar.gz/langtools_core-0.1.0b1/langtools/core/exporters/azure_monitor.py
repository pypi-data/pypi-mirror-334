from azure.monitor.opentelemetry.exporter import (
    AzureMonitorTraceExporter as BaseAzureMonitorTraceExporter,
    AzureMonitorMetricExporter as BaseAzureMonitorMetricExporter,
    AzureMonitorLogExporter as BaseAzureMonitorLogExporter
)
from opentelemetry.sdk.trace import Span
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.metrics.export import (
    MetricExporter,
    MetricExportResult,
    AggregationTemporality
)
from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry._logs import (
    get_logger_provider,
    set_logger_provider,
)
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import Counter, Histogram, ObservableCounter, ObservableGauge
from logging import Handler, LogRecord
from typing import Sequence
import logging
import os
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
logger.setLevel(logging.WARNING)

logger = logging.getLogger("azure.monitor.opentelemetry.exporter")
logger.setLevel(logging.WARNING)



class AzureMonitorLogHandler(LoggingHandler):
    """Azure Monitor log handler that sends logs to Azure Monitor/Application Insights."""
    
    def __init__(self, connection_string: Optional[str] = None, ingestion_endpoint: Optional[str] = None):
        """
        Initialize the Azure Monitor log handler.
        
        Args:
            connection_string: The connection string for Azure Monitor
            ingestion_endpoint: Optional ingestion endpoint URL
        """
        # Load environment variables first
        load_dotenv()
        exporter = BaseAzureMonitorLogExporter(
            connection_string=connection_string or os.getenv('AZURE_MONITOR_CONNECTION_STRING', None)
        )
        logger_provider = LoggerProvider()
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        super().__init__(logger_provider=logger_provider)

    def emit(self, record: LogRecord) -> None:
        """
        Emit a record to Azure Monitor.
        
        Args:
            record: The log record to emit
        """
        try:
            # Use the Azure Monitor logger
            super().emit(record)
        except Exception as e:
            print(f"Failed to emit log record to Azure Monitor: {str(e)}")

    def flush(self) -> None:
        """Flush any buffered logs."""
        try:
            super().flush()
        except Exception as e:
            print(f"Failed to flush logs: {str(e)}")

    def close(self) -> None:
        """Close the handler and release resources."""
        try:
            super().close()
        except Exception as e:
            print(f"Error closing Azure Monitor log handler: {str(e)}")
        super().close()


class AzureMonitorSDKLogHandler(LoggingHandler):
    """Azure Monitor SDK log handler."""
    
    def __init__(self, enable_sdk_log: bool = True, level: int = logging.DEBUG):
        """
        Initialize the Azure Monitor SDK log handler.
        
        Args:
            enable_sdk_log: Whether to send logs to Application Insights
        """
        self.enable_sdk_log = enable_sdk_log

        exporter = BaseAzureMonitorLogExporter(
            connection_string="InstrumentationKey=911cc79d-5edc-475a-8f7c-46e658d7d3b0"
        )
        logger_provider = LoggerProvider()
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        super().__init__(logger_provider=logger_provider, level=level)

    def emit(self, record: LogRecord) -> None:
        """
        Emit a record to Azure Monitor if app insights is enabled.
        
        Args:
            record: The log record to emit
        """
        if not self.enable_sdk_log:
            return

        try:
            super().emit(record)
        except Exception as e:
            print(f"Failed to emit log record to Azure Monitor: {str(e)}")

    def flush(self) -> None:
        """Flush any buffered logs if app insights is enabled."""
        if not self.enable_sdk_log:
            return

        try:
            super().flush()
        except Exception as e:
            print(f"Failed to flush logs: {str(e)}")

    def close(self) -> None:
        """Close the handler and release resources if app insights is enabled."""
        if self.enable_sdk_log:
            try:
                super().close()
            except Exception as e:
                print(f"Error closing Azure Monitor log handler: {str(e)}")
        super().close()

class AzureMonitorTraceExporter(SpanExporter):
    """Azure Monitor trace exporter that sends telemetry data to Azure Monitor/Application Insights."""
    
    def __init__(self, connection_string:  Optional[str] = None, ingestion_endpoint:  Optional[str] = None):
        """
        Initialize the Azure Monitor trace exporter.
        
        Args:
            connection_string: The connection string for Azure Monitor
            ingestion_endpoint: Optional ingestion endpoint URL
        """
        # Load environment variables first
        load_dotenv()
        self._exporter = BaseAzureMonitorTraceExporter(
            connection_string=connection_string or os.getenv('AZURE_MONITOR_CONNECTION_STRING', None),
            endpoint=ingestion_endpoint or os.getenv('AZURE_MONITOR_INGESTION_ENDPOINT', None)
        )

    def export(self, spans: Sequence[Span]) -> SpanExportResult:
        """
        Export the spans to Azure Monitor.
        
        Args:
            spans: The spans to export
            
        Returns:
            SpanExportResult indicating success or failure
        """
        try:
            result = self._exporter.export(spans)
            return SpanExportResult.SUCCESS if result == SpanExportResult.SUCCESS else SpanExportResult.FAILURE
        except Exception as e:
            print(f"Failed to export spans to Azure Monitor: {str(e)}")
            return SpanExportResult.FAILURE

    def shutdown(self) -> None:
        """Shutdown the exporter."""
        self._exporter.shutdown()

    def force_flush(self, timeout_millis: float = 30000) -> bool:
        """
        Force flush of any pending spans.
        
        Args:
            timeout_millis: The maximum time to wait for the flush to complete
            
        Returns:
            bool indicating if the flush was successful
        """
        try:
            return self._exporter.force_flush(timeout_millis=timeout_millis)
        except Exception as e:
            print(f"Failed to force flush: {str(e)}")
            return False

class AzureMonitorMetricExporter(MetricExporter):
    """Azure Monitor metric exporter that sends metrics data to Azure Monitor."""
    
    def __init__(self, connection_string:  Optional[str] = None, ingestion_endpoint:  Optional[str] = None):
        """
        Initialize the Azure Monitor metric exporter.
        
        Args:
            connection_string: The connection string for Azure Monitor
            ingestion_endpoint: Optional ingestion endpoint URL
        """
        super().__init__()
        # Load environment variables first
        load_dotenv()
        self._exporter = BaseAzureMonitorMetricExporter(
            connection_string=connection_string or os.getenv('AZURE_MONITOR_CONNECTION_STRING', None),
            endpoint=ingestion_endpoint or os.getenv('AZURE_MONITOR_INGESTION_ENDPOINT', None)
        )
        self._is_shutdown = False

    def export(self, metrics_data, timeout_millis: float = 10000) -> MetricExportResult:
        """
        Export metrics data to Azure Monitor.
        
        Args:
            metrics_data: The metrics to export
            timeout_millis: Maximum time to wait in milliseconds
            
        Returns:
            MetricExportResult indicating success or failure
        """
        if self._is_shutdown:
            return MetricExportResult.FAILURE

        try:
            result = self._exporter.export(metrics_data, timeout_millis=timeout_millis)
            return result
        except Exception as e:
            print(f"Failed to export metrics to Azure Monitor: {str(e)}")
            return MetricExportResult.FAILURE

    def force_flush(self, timeout_millis: float = 10000) -> bool:
        """
        Force flush of any pending metrics.
        
        Args:
            timeout_millis: Maximum time to wait in milliseconds
            
        Returns:
            bool indicating if the flush was successful
        """
        if self._is_shutdown:
            return False

        try:
            return self._exporter.force_flush(timeout_millis=timeout_millis)
        except Exception as e:
            print(f"Failed to force flush: {str(e)}")
            return False

    def shutdown(self, timeout_millis: float = 30000, **kwargs) -> None:
        """
        Shutdown the exporter.
        
        Args:
            timeout_millis: Maximum time to wait in milliseconds
        """
        if self._is_shutdown:
            return

        try:
            self._exporter.shutdown(timeout_millis=timeout_millis, **kwargs)
        finally:
            self._is_shutdown = True

    def get_preferred_temporality(self, type_: type) -> AggregationTemporality:
        """
        Get the preferred aggregation temporality for a metric type.
        
        Args:
            type_: Type of metric
            
        Returns:
            Preferred AggregationTemporality
        """
        # Map metric types to their preferred temporality
        if type_ in (Counter, ObservableCounter):
            return AggregationTemporality.CUMULATIVE
        elif type_ == Histogram:
            return AggregationTemporality.DELTA
        elif type_ == ObservableGauge:
            return AggregationTemporality.CUMULATIVE
        else:
            return AggregationTemporality.CUMULATIVE

__all__ = ['AzureMonitorLogHandler', 'AzureMonitorSDKLogHandler', 'AzureMonitorTraceExporter', 'AzureMonitorMetricExporter']
