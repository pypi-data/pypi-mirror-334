from typing import List, Optional, Sequence, Callable
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    MetricExporter,
    PeriodicExportingMetricReader,
)
from .exporters.noop_exporter import NoOpMetricExporter
from opentelemetry.sdk.metrics.view import View
import json
import time
from dataclasses import dataclass, asdict
import threading

@dataclass
class MetricAttribute:
    """Class representing metric attributes."""
    name: str
    value: str

class Meter:
    """Meter class for metrics tracking following the specification."""
    
    _provider = None
    _instance = None
    _exporters = []

    @classmethod
    def initMeter(cls, 
                 service_name: str,
                 exporters: List[MetricExporter] = None, 
                 export_interval_millis: float = 60000,
                 export_timeout_millis: float = 30000) -> None:
        """
        Initialize meter with specified exporters and configuration.
        
        Args:
            exporters: List of exporters for metrics data
            export_interval_millis: Export interval in milliseconds
            export_timeout_millis: Export timeout in milliseconds
        """
        if exporters is None:
            exporters = [NoOpMetricExporter()]
        
        cls._exporters = exporters
        
        # Create readers with delta temporality for better aggregation
        readers = [
            PeriodicExportingMetricReader(
                exporter,
                export_interval_millis=export_interval_millis,
                export_timeout_millis=export_timeout_millis,
            ) for exporter in exporters
        ]

        # Create and set MeterProvider
        cls._provider = MeterProvider(resource = Resource(attributes={
                                        SERVICE_NAME: service_name
                                    }), metric_readers=readers)
        set_meter_provider(cls._provider)

    @classmethod
    def getMeter(cls, name: Optional[str] = None) -> 'Meter':
        """
        Get a meter instance.
        
        Args:
            name: Name for the meter
            
        Returns:
            Meter instance
        """
        if cls._provider is None:
            cls.initMeter(name or "root")
            
        instance = cls()
        instance._meter = get_meter_provider().get_meter(name or __name__)
        return instance

    def __init__(self):
        """Initialize a new Meter instance."""
        self._meter = None
        self._views = {}

    def create_counter(self, name: str, unit: str = "", description: str = ""):
        """Create a Counter instrument."""
        return self._meter.create_counter(
            name,
            unit=unit,
            description=description
        )

    def create_up_down_counter(self, name: str, unit: str = "", description: str = ""):
        """Create an UpDownCounter instrument."""
        return self._meter.create_up_down_counter(
            name,
            unit=unit,
            description=description
        )

    def create_observable_counter(self, name: str, callbacks: Sequence[Callable] = None,
                                unit: str = "", description: str = ""):
        """Create an ObservableCounter instrument."""
        return self._meter.create_observable_counter(
            name,
            callbacks=callbacks,
            unit=unit,
            description=description
        )

    def create_histogram(self, name: str, unit: str = "", description: str = ""):
        """Create a Histogram instrument."""
        return self._meter.create_histogram(
            name,
            unit=unit,
            description=description
        )

    def create_gauge(self, name: str, unit: str = "", description: str = ""):
        """Create a Gauge instrument."""
        return self._meter.create_observable_gauge(
            name,
            unit=unit,
            description=description
        )

    def create_observable_gauge(self, name: str, callbacks: Sequence[Callable] = None,
                              unit: str = "", description: str = ""):
        """Create an ObservableGauge instrument."""
        return self._meter.create_observable_gauge(
            name,
            callbacks=callbacks,
            unit=unit,
            description=description
        )

    def create_observable_up_down_counter(self, name: str, callbacks: Sequence[Callable] = None,
                                        unit: str = "", description: str = ""):
        """Create an ObservableUpDownCounter instrument."""
        return self._meter.create_observable_up_down_counter(
            name,
            callbacks=callbacks,
            unit=unit,
            description=description
        )

    @classmethod
    def shutdown(cls):
        """Shutdown all exporters."""
        for exporter in cls._exporters:
            try:
                exporter.shutdown()
            except Exception as e:
                print(f"Error shutting down exporter: {str(e)}")

