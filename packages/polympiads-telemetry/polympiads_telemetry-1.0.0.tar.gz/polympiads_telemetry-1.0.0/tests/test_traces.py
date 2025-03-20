
import time
from unittest.mock import patch, Mock

from telemetry import using_test_config
from telemetry.config import HttpConfig
from telemetry.config import TestConfig as _TestConfig
from telemetry.traces import TraceTestVerbosity, VirtualContext, configure_test, configure_http, get_test_exporter, get_tracer

@patch("telemetry.traces.TracerProvider")
@patch("telemetry.traces.BatchSpanProcessor")
@patch("telemetry.traces.HTTPExporter")
@patch("opentelemetry.trace.set_tracer_provider")
def test_configure_http (
        set_tracer_provider: Mock, http_exporter: Mock,
        batch_processor : Mock, tracer_provider : Mock):
    tracer_provider.return_value = Mock()
    tracer_provider.return_value.add_span_processor = Mock()

    http_exporter  .return_value = Mock()
    batch_processor.return_value = Mock()

    http_config = HttpConfig( "http://localhost:4318" )
    configure_http(http_config)

    set_tracer_provider.assert_called_once_with( tracer_provider.return_value )
    tracer_provider.return_value.add_span_processor \
        .assert_called_once_with( batch_processor.return_value )
    batch_processor.assert_called_once_with( http_exporter.return_value )
    http_exporter.assert_called_once_with( http_config.traces_endpoint )
    tracer_provider.assert_called_once_with( resource=http_config.resource )

@patch("telemetry.traces.TracerProvider")
@patch("telemetry.traces.SimpleSpanProcessor")
@patch("opentelemetry.trace.set_tracer_provider")
def test_configure_test (set_tracer_provider: Mock, simple_processor: Mock, tracer_provider: Mock):
    tracer_provider.return_value = Mock()
    tracer_provider.return_value.add_span_processor = Mock()
    simple_processor.return_value = Mock()
    set_tracer_provider.return_value = Mock()

    test_config = _TestConfig()
    configure_test(test_config)

    set_tracer_provider.assert_called_once_with( tracer_provider.return_value )
    tracer_provider.return_value.add_span_processor \
        .assert_called_once_with( simple_processor.return_value )
    simple_processor.assert_called_once_with( get_test_exporter() )
    tracer_provider.assert_called_once_with(resource=test_config.resource)

TRACE_SCHEME = """
+    Span  "some_span" [some_attr:1][other_attr:abcd]
|    Event "e1"    
| +  Span  "other_span" [one_attr:42]
| |  Event "e2"
| +
|    Event "e3" [eattr:R]
+
"""
EXPECTED_FULL_VERBOSITY = """===== EXPECTED =====
+    Span  "some_span" [other_attr:abcd][some_attr:1]
|    Event "e1"
| +  Span  "other_span" [one_attr:42]
| |  Event "e2"
| +  
|    Event "e3" [eattr:R]
+    

===== FOUND =====
+    Span  "some_span" [other_attr:abcd][some_attr:1]
|    Event "e3"
| +  Span  "other_span" [one_attr:42]
| |  Event "e2"
| +  
|    Event "e1" [eattr:R]
+    

Warning, in case of short time spans, the scheme might look different
But they might be equivalent in the match.
"""

@using_test_config
def test_traces ():
    tracer = get_tracer("tests")

    with tracer.start_as_current_span("some_span") as some_span:
        some_span.add_event("e1")
        with tracer.start_as_current_span("other_span") as other_span:
            other_span.add_event("e2")
            other_span.set_attribute("one_attr", 42)
        some_span.add_event("e3", { "eattr": "R" })
        some_span.set_attribute("some_attr", 1)
        some_span.set_attribute("other_attr", "abcd")

    exporter = get_test_exporter()
    spans = exporter.get_finished_spans()
    exporter.clear()
    if spans[0].parent is None:
        a, b = spans
        spans = a, b

    assert len(spans) == 2
    assert spans[0].parent == spans[1].context

    child = spans[0]
    root  = spans[1]

    assert child.name == "other_span"
    assert len(child.events) == 1

    event2 = child.events[0]
    assert event2.name == "e2"
    assert child.attributes == { "one_attr": 42 }

    assert root.name == "some_span"
    assert len(root.events) == 2

    event1, event3 = root.events
    assert event1.name == "e1"
    assert event3.name == "e3"
    assert event3.attributes == { "eattr": "R" }

    assert root.attributes == { "some_attr": 1, "other_attr": "abcd" }

@using_test_config
def test_traces_with_scheme ():
    tracer = get_tracer("tests")

    with tracer.start_as_current_span("some_span") as some_span:
        some_span.add_event("e1")
        time.sleep(0.01)
        with tracer.start_as_current_span("other_span") as other_span:
            other_span.add_event("e2")
            time.sleep(0.01)
            other_span.set_attribute("one_attr", 42)
        some_span.add_event("e3", { "eattr": "R" })
        time.sleep(0.01)
        some_span.set_attribute("some_attr", 1)
        some_span.set_attribute("other_attr", "abcd")

    ctx1 = VirtualContext.from_exporter()
    ctx2 = VirtualContext.from_scheme(TRACE_SCHEME)
    assert ctx1.match_with(ctx2)
@using_test_config
def test_traces_with_scheme_instant ():
    tracer = get_tracer("tests")

    with tracer.start_as_current_span("some_span") as some_span:
        some_span.add_event("e1")
        with tracer.start_as_current_span("other_span") as other_span:
            other_span.add_event("e2")
            other_span.set_attribute("one_attr", 42)
        some_span.add_event("e3", { "eattr": "R" })
        some_span.set_attribute("some_attr", 1)
        some_span.set_attribute("other_attr", "abcd")
    
    exporter = get_test_exporter()
    for span in exporter.get_finished_spans():
        span._start_time = span._end_time = 0
        for event in span.events:
            event._timestamp = 0
    
    ctx1 = VirtualContext.from_exporter()
    ctx2 = VirtualContext.from_scheme(TRACE_SCHEME)
    assert ctx1.match_with(ctx2)
@using_test_config
def test_traces_with_scheme_wrong_order (capsys):
    tracer = get_tracer("tests")

    with tracer.start_as_current_span("some_span") as some_span:
        some_span.add_event("e3")
        time.sleep(0.01)
        with tracer.start_as_current_span("other_span") as other_span:
            time.sleep(0.01)
            other_span.add_event("e2")
            other_span.set_attribute("one_attr", 42)
        time.sleep(0.01)
        some_span.add_event("e1", { "eattr": "R" })
        some_span.set_attribute("some_attr", 1)
        some_span.set_attribute("other_attr", "abcd")
    
    assert not VirtualContext.verify_scheme(TRACE_SCHEME, TraceTestVerbosity.FULL)
    assert capsys.readouterr().out == EXPECTED_FULL_VERBOSITY
@using_test_config
def test_traces_with_scheme_no_verbose (capsys):
    tracer = get_tracer("tests")

    with tracer.start_as_current_span("some_span") as some_span:
        some_span.add_event("e3")
        time.sleep(0.01)
        with tracer.start_as_current_span("other_span") as other_span:
            time.sleep(0.01)
            other_span.add_event("e2")
            other_span.set_attribute("one_attr", 42)
        time.sleep(0.01)
        some_span.add_event("e1", { "eattr": "R" })
        some_span.set_attribute("some_attr", 1)
        some_span.set_attribute("other_attr", "abcd")
    
    assert not VirtualContext.verify_scheme(TRACE_SCHEME)
    assert capsys.readouterr().out == ""

SIMPLE_TRACE_SCHEME = """
+ Span  "na" [a:a]
| Event "nb" [a:a]
+
"""
def simple_trace (na: str = "na", aa: str = "a", nb: str = "nb", ba: str = "a"):
    tracer = get_tracer("tests")
    with tracer.start_as_current_span(na) as some_span:
        if aa is not None:
            some_span.set_attribute("a", aa)
        if nb is not None:
            if ba is not None:
                some_span.add_event(nb, { "a": ba })
            else:
                some_span.add_event(nb)

@using_test_config
def test_tracer_sort ():
    tracer = get_tracer("tests")
    
    with tracer.start_as_current_span("some_span") as some_span: pass
    time.sleep(0.01)
    with tracer.start_as_current_span("other_span") as some_span: pass

    ctx = VirtualContext.from_exporter()
    sp, ot = ctx.roots
    assert sp < ot and not (ot < sp)
    sp.start_time = ot.start_time
    assert sp < ot and not (ot < sp)
    sp.end_time = ot.end_time
    assert not (sp < ot) and not (ot < sp)

@using_test_config
def test_simple_trace_scheme ():
    simple_trace()
    assert VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
@using_test_config
def test_simple_trace_scheme_wrong ():
    simple_trace(nb = "en")
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    simple_trace(ba = "vn")
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    simple_trace(ba = None)
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    simple_trace(nb = None)
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    simple_trace(aa = None)
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    simple_trace(aa = "va")
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    simple_trace(na = "va")
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)
    
    tracer = get_tracer("tests")
    with tracer.start_as_current_span("na") as span:
        span.set_attribute("a", "a")
        span.add_event("nb", { "a": "a" })
        with tracer.start_as_current_span("a"):
            pass
    assert not VirtualContext.verify_scheme(SIMPLE_TRACE_SCHEME)