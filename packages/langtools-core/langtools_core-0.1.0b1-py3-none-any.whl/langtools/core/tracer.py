# Standard library imports
from functools import wraps
from typing import List, Optional, Any, Dict, Callable, AsyncGenerator
from datetime import datetime
import uuid
import asyncio
import orjson
from datetime import datetime
from typing import Callable, Dict
from opentelemetry import trace, context
from opentelemetry.sdk.trace import Span, TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SimpleSpanProcessor,
)
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.completion import Completion
from opentelemetry.trace import SpanKind, StatusCode
from .utils.serializer import to_serializable, get_attr
from .utils.openai_result_parser import OpenAIResponseParser, collect_openai_tokens, collect_openai_tokens_for_streaming
from .exporters.noop_exporter import NoOpTraceExporter
from .logger import SDKLogger

class Tracer:
    """A tracer class that supports multiple exporters and different types of spans."""

    _provider = None
    _instance = None

    @classmethod
    def initTracer(cls, service_name: str, exporters: Optional[List[SpanExporter]] = None) -> None:
        """Initialize tracer with specified exporters.
        
        Args:
            service_name: Name of the service being traced.
            exporters: List of exporters for span information. Defaults to [NoOpTraceExporter()].
        """
        cls._provider = TracerProvider(
            resource=Resource(attributes={SERVICE_NAME: service_name})
        )
        trace.set_tracer_provider(cls._provider)
        
        # Use default exporter if none provided
        actual_exporters = exporters or [NoOpTraceExporter()]
        
        for exporter in actual_exporters:
            processor = SimpleSpanProcessor(exporter)
            cls._provider.add_span_processor(processor)

    @classmethod
    def getTracer(cls, name: Optional[str] = None) -> 'Tracer':
        """Get a tracer instance, initializing provider if needed.
        
        Args:
            name: Name for the tracer. Defaults to module name.
            
        Returns:
            Tracer instance
        """
        if cls._provider is None:
            cls.initTracer(name or "root")
        
        instance = cls()
        instance._tracer = cls._provider.get_tracer(name or __name__)
        return instance

    def __init__(self):
        """Initialize a new Tracer instance."""
        self._tracer = None  # Will be set by getTracer

    def _create_common_attributes(self, func: Callable, start_time: datetime, args: tuple, kwargs: dict) -> Dict:
        """Create common span attributes shared between all spans.
        
        Args:
            func: The function being traced
            start_time: When the function started
            args: Function arguments
            kwargs: Function keyword arguments
            
        Returns:
            Dictionary of common attributes
        """
        duration = datetime.now() - start_time
        session_id = uuid.uuid4()
        SDKLogger.getSdklogger().info(f"Tracing function call {func.__code__.co_filename} - {func.__name__} in line {func.__code__.co_firstlineno}", 
                                      extra={ 
                                          "function": func.__name__,
                                          "duration": str(duration), 
                                          "session_id": str(session_id), })
        return {
            "duration": str(duration),
            "session_id": str(session_id),
            "code": orjson.dumps({
                "file": func.__code__.co_filename,
                "line": func.__code__.co_firstlineno,
                "name": func.__name__
            }),
            "inputs": orjson.dumps({
                "args": to_serializable(args),
                "kwargs": to_serializable(kwargs)
            })
        }

    def _set_span_attributes(self, span: Span, func: Callable, start_time: datetime, 
                           args: tuple, kwargs: dict, result: Any, 
                           additional_attributes: Optional[Dict] = None, 
                           span_type: Optional[str] = None) -> None:
        """Set all span attributes.
        
        Args:
            span: The span to set attributes on
            func: The function being traced
            start_time: When the function started
            args: Function arguments
            kwargs: Function keyword arguments
            result: Function result
            additional_attributes: Extra attributes to set
            span_type: Type of span
        """
        # Set common attributes
        common_attrs = self._create_common_attributes(func, start_time, args, kwargs)
        for key, value in common_attrs.items():
            span.set_attribute(key, value)

        # Set span type
        if span_type:
            span.set_attribute("span_type", span_type)

        if span_type == "LLM":
            self.enrich_llm(span, args, kwargs, result)
        else:
            output = to_serializable(result)
            span.set_attribute("outputs", orjson.dumps(to_serializable(output)))
            # Set additional attributes
            if additional_attributes:
                for key, value in additional_attributes.items():
                    try:
                        if callable(value):
                            attr_value = value(result)
                            if attr_value is not None:
                                span.set_attribute(key, attr_value)
                    except (AttributeError, KeyError):
                        continue

    def _create_span_decorator(self, span_type: str, additional_attributes: Optional[Dict] = None):
        """Create a decorator for tracing functions with specific span type.
        
        Args:
            span_type: Type of span to create
            additional_attributes: Extra attributes to set on span
            
        Returns:
            Function decorator
        """
        async def handle_stream(result, span, token, func, start_time, args, kwargs):
            try:
                # Collect streamed items while yielding
                streamed_items = []
                async for item in result:
                    streamed_items.append(item)
                    yield item
                # Set the collected stream items
                span.set_status(StatusCode.OK)
            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                raise
            finally:
                # Set attributes before span ends
                self._set_span_attributes(
                    span, func, start_time, args, kwargs,
                    streamed_items, additional_attributes, span_type
                )
                span.end()

        def decorator(func):
            if asyncio.iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    start_time = datetime.now()
                    span = self._tracer.start_span(
                            name=func.__name__,
                            kind=SpanKind.CONSUMER,
                        )
                    ctx = trace.set_span_in_context(span)
                    token = context.attach(ctx)
                    try:
                        result = await func(*args, **kwargs)
                        try:
                            if isinstance(result, AsyncGenerator):
                                return handle_stream(result, span, token, func, start_time, args, kwargs)
                            else:
                                self._set_span_attributes(
                                    span, func, start_time, args, kwargs,
                                    result, additional_attributes, span_type
                                )
                                span.set_status(StatusCode.OK)
                                span.end()
                        except Exception as e:
                            span.end()
                        
                        return result
                    except Exception as e:
                        span.set_status(StatusCode.ERROR, str(e))
                        span.end()
                        raise
                    finally:
                        context.detach(token)
                
                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    with self._tracer.start_as_current_span(
                        name=func.__name__,
                        kind=SpanKind.CONSUMER,
                    ) as span:
                        start_time = datetime.now()
                        try:
                            result = func(*args, **kwargs)
                            self._set_span_attributes(
                                span, func, start_time, args, kwargs,
                                result, additional_attributes, span_type
                            )
                            span.set_status(StatusCode.OK)
                            return result
                        except Exception as e:
                            span.set_status(StatusCode.ERROR, str(e))
                            raise
                
                return sync_wrapper
            
        return decorator

    def trace(self, func):
        """Decorator for tracing generic functions."""
        return self._create_span_decorator("Function")(func)

    def llm(self, func):
        """Decorator for tracing LLM operations."""
        return self._create_span_decorator("LLM")(func)
    
    def enrich_llm(self, span, args, kwargs, output):
        from openai.types.chat.chat_completion import ChatCompletion
        from openai.types.completion import Completion

        if isinstance(output, (ChatCompletion, Completion)):
            model = output.model if isinstance(output, (ChatCompletion, Completion)) else None
            if isinstance(output, ChatCompletion):
                generated_message = output.choices[0].message
            elif isinstance(output, Completion):
                generated_message = output.choices[0].text
            else:
                generated_message = None
            token = collect_openai_tokens(output)

        elif isinstance(output, list) and len(output) > 0 and isinstance(output[0], (ChatCompletionChunk, Completion)):
            # For streaming LLM responses, set attributes before stream ends
            token = collect_openai_tokens_for_streaming(kwargs, output, True)
            
            parser = OpenAIResponseParser.init_parser(output)
            model = parser.model
            generated_message = to_serializable(parser.get_generated_message())
        else:
            token = {
                "total_tokens": get_attr(get_attr(output, 'usage', None), "total_tokens", None),
                "prompt_tokens": get_attr(get_attr(output, 'usage', None), "prompt_tokens", None),
                "completion_tokens": get_attr(get_attr(output, 'usage', None), "completion_tokens", None)
            }
            model = get_attr(output, "model", None)
            generated_message = get_attr(get_attr(output, "choices", None)[0], "text", None)

        span.set_attribute("llm.usage.total_tokens", token.get("total_tokens", None))
        span.set_attribute("llm.usage.prompt_tokens", token.get("prompt_tokens", None))
        span.set_attribute("llm.usage.completion_tokens", token.get("completion_tokens", None))
        span.set_attribute("llm.response.model", model)
        span.set_attribute("outputs", orjson.dumps(to_serializable(generated_message)))

    def search(self, func):
        """Decorator for tracing search operations."""
        return self._create_span_decorator("Search", {
            "answers.counts": lambda r: len(get_attr(get_attr(r.json(), 'value', {}), 'answers', [])),
            "answers":lambda r: orjson.dumps(get_attr(get_attr(r.json(), 'value', {}), 'answers', []))
        })(func)

    def embedding(self, func):
        """Decorator for tracing embedding operations."""
        return self._create_span_decorator("Embedding", {
            "embedding.embeddings": lambda r: orjson.dumps([
                item.embedding for item in get_attr(r, 'data', [])
            ] if get_attr(r, 'data', None) else None),
            "llm.usage.total_tokens": lambda r: get_attr(get_attr(r, 'usage', None), 'total_tokens', None),
            "llm.usage.prompt_tokens": lambda r: get_attr(get_attr(r, 'usage', None), 'prompt_tokens', None),
            "llm.response.model": lambda r: get_attr(r, 'model', 'unknown')
        })(func)