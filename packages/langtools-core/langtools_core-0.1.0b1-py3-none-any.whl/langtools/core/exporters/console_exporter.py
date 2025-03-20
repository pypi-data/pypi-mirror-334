import sys
from logging import StreamHandler
from typing import Optional
import typing
import orjson
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter as BaseConsoleSpanExporter
from opentelemetry.sdk.trace import ReadableSpan

class ConsoleLogHandler(StreamHandler):
    """Handler that writes log records to the console."""
    def __init__(self):
        """Initialize the handler."""
        super().__init__(sys.stdout)

class ConsoleSpanExporter(BaseConsoleSpanExporter):
    """Implementation of ConsoleSpanExporter that properly handles Chinese text.
    
    This exporter ensures proper formatting of Chinese characters in the console output
    without relying on unicode escape sequences.
    """
    
    def __init__(
        self,
        service_name: Optional[str] = None,
        out: typing.IO = sys.stdout
    ):
        def formatter(span: ReadableSpan) -> str:
            # Convert span to dictionary
            span_dict = orjson.loads(span.to_json())
            # Ensure proper encoding of Chinese characters
            return orjson.dumps(span_dict, option=orjson.OPT_APPEND_NEWLINE|orjson.OPT_INDENT_2).decode('utf-8')
            
        super().__init__(
            service_name=service_name,
            out=out,
            formatter=formatter
        )

# Re-export the OpenTelemetry exporters with our Chinese-adapted version as default
__all__ = ['ConsoleLogHandler', 'ConsoleMetricExporter', 'ConsoleSpanExporter']
