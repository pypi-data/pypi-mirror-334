# LangTools Core SDK

## Background

LangTools vNext is a project aimed at enhancing developer experience in MAI, enabling faster experimentation and deployment of Generative AI-based features to swiftly deliver increased value to our users. The langtools-core SDK, serving as the foundation for LangTools vNext, offers essential tools for building services/GenAI applications, including AI-aware logging, tracing, metrics tracking, debugging, and evaluation.

## Goal

- Define the developer's experience of this package.
- Define the functionality that the package should provide.
- Design the user experience of the functionality such as logging, tracing, metrics tracking, and evaluation.
- Identify the dependencies required by the package.
- Propose public interfaces exposed by the package.

## Non-Goal

- Design of predefined metrics.
- Prompty should not be included in the package, users can decide whether to leverage it.

## Proposal

Langtools-core SDK is a Python package that will be published to PyPI. A .NET version will be supported in the future.

| Package         | Functionality             | Imports (SDK)                      |
|-----------------|---------------------------|------------------------------------|
| langtools-core  | Logging capability        | from langtools.core import Logger  |
|                 | Tracing capability        | from langtools.core import Tracer  |
|                 | Metrics tracking capability | from langtools.core import Meter   |

For detailed documentation on each component, please refer to the docs in the [docs/core](../../docs/core) directory:
- [Logger Documentation](../../docs/core/Logger.md)
- [Tracer Documentation](../../docs/core/Tracer.md)
- [Meter Documentation](../../docs/core/Meter.md)

### Package Structure

```
langtools.core
├── logger.py         # Main logger implementation
├── tracer.py         # Main tracer implementation
├── meter.py          # Main meter implementation
├── credential.py     # Main credential implementation
└── exporters/        # Built-in exporters
    ├── __init__.py
    ├── console_exporter.py
    ├── file_exporter.py
    └── azure_monitor.py
    └── noop_exporter.py
└── identity/        # Built-in identity
    ├── __init__.py
    ├── LongRunningOBOTokenCredential.py
└── utils/
    ├── openai_result_parser.py
    ├── serializer.py
```

### Basic Usage Example

```python
from langtools.core import Logger, Tracer, Meter
from langtools.core.exporters import ConsoleLogHandler, ConsoleSpanExporter, ConsoleMetricExporter
# Set up logger
Logger.basicConfig(handlers=[ConsoleLogHandler()])
logger = Logger.getLogger(__name__)

# Set up tracer
Tracer.initTracer("my-service", [ConsoleSpanExporter()])
tracer = Tracer.getTracer(__name__)

# Set up meter
Meter.initMeter("my-service", [ConsoleMetricExporter()])
meter = Meter.getMeter(__name__)

# Example usage
@tracer.trace
def example_function():
    logger.info("Starting example function")
    counter = meter.create_counter("function_calls")
    counter.add(1)
    logger.info("Finished example function")

example_function()
```

For more detailed examples and API documentation for each component, please refer to the individual documentation files in the [docs/core](../../docs/core) directory.
