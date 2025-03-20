from opentelemetry.sdk.trace import Span
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from typing import Sequence
import json
import os
import threading
from queue import Queue, Empty
import time
from logging import FileHandler
from opentelemetry.sdk.metrics.export import (
    MetricExporter,
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
    MetricExportResult,
    AggregationTemporality,
)


class FileLogHandler(FileHandler):
    """Handler that writes log records to a file."""
    def __init__(self, filename: str, mode: str = 'a', encoding: str = 'utf-8'):
        """
        Initialize the handler.
        
        Args:
            filename: Path to the log file
            mode: Mode to open the file ('a' for append)
            encoding: Text encoding to use
        """
        # Create directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        super().__init__(filename, mode, encoding)
        self._lock = threading.Lock()
        
'''
class FileSpanExporter(SpanExporter):
    """
    File-based span exporter that exports spans to a specified file.
    """
    
    def __init__(self, filename: str):
        """
        Initialize the file exporter.
        
        Args:
            filename: Path to the file where spans will be written
        """
        self.filename = filename
        self._is_shutdown = False
        self._pending_spans = Queue()
        self._export_lock = threading.Lock()
        
        # Ensure directory exists
        directory = os.path.dirname(os.path.abspath(filename))
        if directory:  # Only create if there's a directory part
            os.makedirs(directory, exist_ok=True)
            
        # Create or truncate the file
        with open(filename, "w", encoding="utf-8") as f:
            f.write("")  # Ensure the file exists and is empty

    def export(self, spans: Sequence[Span]) -> SpanExportResult:
        """
        Export the spans to a file.
        
        Args:
            spans: List of spans to export
            
        Returns:
            SpanExportResult indicating success or failure
        """
        if self._is_shutdown:
            print("Exporter is shutdown, refusing to export spans.")
            return SpanExportResult.FAILURE

        try:
            with self._export_lock:
                for span in spans:
                    self._pending_spans.put(span)
                
                return self._flush_spans()
        except Exception as e:
            print(f"Failed to export spans to file: {str(e)}")
            return SpanExportResult.FAILURE

    def _flush_spans(self) -> SpanExportResult:
        """
        Flush pending spans to the file.
        
        Returns:
            SpanExportResult indicating success or failure
        """
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                while not self._pending_spans.empty():
                    try:
                        span = self._pending_spans.get_nowait()
                        
                        # Convert span to dictionary
                        span_dict = {
                            "name": span.name,
                            "context": {
                                "trace_id": format(span.context.trace_id, "x"),
                                "span_id": format(span.context.span_id, "x"),
                            },
                            "kind": span.kind.name,
                            "start_time": span.start_time,
                            "end_time": span.end_time,
                            "attributes": dict(span.attributes),
                            "status": span.status.status_code.name,
                        }
                        
                        # Write to file and ensure it's written to disk
                        f.write(json.dumps(span_dict, indent=2) + "\n\n")
                        f.flush()
                        os.fsync(f.fileno())
                        
                        self._pending_spans.task_done()
                    except Empty:
                        break
                    
            return SpanExportResult.SUCCESS
        except Exception as e:
            print(f"Failed to flush spans to file: {str(e)}")
            return SpanExportResult.FAILURE

    def shutdown(self) -> None:
        """
        Shuts down the exporter. After this is called, the exporter will refuse
        new exports and will flush any pending spans.
        """
        if self._is_shutdown:
            return

        try:
            # Attempt to flush any pending spans
            with self._export_lock:
                if not self._pending_spans.empty():
                    print(f"Flushing {self._pending_spans.qsize()} pending spans before shutdown...")
                    self._flush_spans()
                    self._pending_spans.join()  # Wait for all spans to be processed
                
        except Exception as e:
            print(f"Error during final flush in shutdown: {str(e)}")
        finally:
            self._is_shutdown = True
            print(f"FileSpanExporter for {self.filename} has been shut down.")

    def force_flush(self, timeout_millis: float = 30000) -> bool:
        """
        Force flush any pending spans. For file-based export, this ensures
        the file is synced to disk.
        
        Args:
            timeout_millis: Maximum time to wait in milliseconds.
            
        Returns:
            bool indicating if the flush was successful
        """
        if self._is_shutdown:
            print("Cannot force flush: exporter is shut down.")
            return False

        try:
            deadline = time.time() + (timeout_millis / 1000.0)
            
            with self._export_lock:
                result = self._flush_spans()
                if result != SpanExportResult.SUCCESS:
                    return False
                
                # Wait for any remaining spans to be processed
                remaining = max(0, deadline - time.time())
                if remaining > 0:
                    self._pending_spans.join()
                
            return True
        except Exception as e:
            print(f"Failed to force flush: {str(e)}")
            return False

       
class FileMetricExporter(MetricExporter):
    """Exporter that writes metrics to a file."""
    
    def __init__(self, filename: str):
        """
        Initialize the exporter.
        
        Args:
            filename: Path to the metrics file
        """
        super().__init__()
        self.filename = filename
        self._lock = threading.Lock()
        self._metrics_cache = {}
        
        # Create directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    def export(self, metrics_data, timeout_millis: float = 10000) -> MetricExportResult:
        """Export metrics data to file."""
        try:
            with self._lock:
                with open(self.filename, "w", encoding="utf-8") as f:
                    # metrics_json = {
                    #     "timestamp": time.time(),
                    #     "metrics": []
                    # }
                    
                    # for rm in metrics_data.resource_metrics:
                    #     for sm in rm.scope_metrics:
                    #         for metric in sm.metrics:
                    #             metric_data = {
                    #                 "name": metric.name,
                    #                 "description": metric.description,
                    #                 "unit": metric.unit,
                    #             }
                                
                    #             # Handle different types of metrics
                    #             if hasattr(metric.data, "points"):
                    #                 points_data = []
                    #                 for point in metric.data.points:
                    #                     point_data = {
                    #                         "value": point.value,
                    #                         "attributes": dict(point.attributes),
                    #                         "timestamp": point.timestamp
                    #                     }
                    #                     if hasattr(point, "bucket_counts"):
                    #                         point_data["bucket_counts"] = point.bucket_counts
                    #                         point_data["bounds"] = point.bounds
                    #                     points_data.append(point_data)
                    #                 metric_data["points"] = points_data

                    #             metrics_json["metrics"].append(metric_data)
                    
                    # json.dump(metrics_json, f, indent=2)
                    # f.write("\n")
                    metrics_data = metrics_data.to_json()
                    f.write(metrics_data)
                    
            return MetricExportResult.SUCCESS
        except Exception as e:
            print(f"Failed to export metrics: {str(e)}")
            return MetricExportResult.FAILURE

    def shutdown(self, timeout_millis: float = 30000, **kwargs) -> None:
        """Shutdown the exporter."""
        self.force_flush(timeout_millis)

    def force_flush(self, timeout_millis: float = 10000) -> bool:
        """Force flush any pending metrics."""
        return True
'''
