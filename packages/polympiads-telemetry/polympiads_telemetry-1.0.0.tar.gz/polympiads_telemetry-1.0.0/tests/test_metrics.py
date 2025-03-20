
from unittest.mock import patch, Mock

from telemetry import using_test_config
from telemetry.config import HttpConfig
from telemetry.config import TestConfig as _TestConfig
from telemetry.metrics import CollectedMetrics, MetricsTestVerbosity, configure_http, configure_test, get_test_reader, get_meter

from opentelemetry.sdk.metrics import MeterProvider

@patch("telemetry.metrics.MeterProvider")
@patch("opentelemetry.metrics.set_meter_provider")
def test_configure_test (set_meter_provider: Mock, meter_provider: Mock):
    meter_provider.return_value = Mock()
    config = _TestConfig()
    configure_test(config)

    meter_provider.assert_called_once_with(resource=config.resource, metric_readers=[get_test_reader()])
    set_meter_provider.assert_called_once_with(meter_provider.return_value)

@patch("telemetry.metrics.MeterProvider")
@patch("telemetry.metrics.PeriodicExportingMetricReader")
@patch("telemetry.metrics.HTTPExporter")
@patch("opentelemetry.metrics.set_meter_provider")
def test_configure_http (set_meter_provider: Mock, otlp_exporter: Mock, periodic_reader: Mock, meter_provider: Mock):
    otlp_exporter.return_value   = Mock()
    periodic_reader.return_value = Mock()
    meter_provider.return_value  = Mock()

    config = HttpConfig("http://localhost:4318")

    configure_http( config )
    set_meter_provider.assert_called_once_with( meter_provider.return_value )
    meter_provider    .assert_called_once_with( resource=config.resource, metric_readers=[ periodic_reader.return_value ] )
    periodic_reader   .assert_called_once_with( otlp_exporter.return_value )
    otlp_exporter     .assert_called_once_with( "http://localhost:4318/v1/metrics" )

@using_test_config
def test_metrics ():
    reader = get_test_reader()

    meter = get_meter("tests")
    gauge = meter.create_gauge("some_gauge", description="Some example gauge")

    gauge.set(1, {  })
    gauge.set(1.5, { "f1": "hello" })

    metrics_data = reader.get_metrics_data()
    resource = metrics_data.resource_metrics[0]
    metrics = resource.scope_metrics[0].metrics
    
    assert len(metrics) == 1
    metric = metrics[0]

    assert metric.name == "some_gauge"
    assert metric.description == "Some example gauge"
    data_points = metric.data.data_points
    
    assert len(data_points) == 2

    keys = {}
    for data_point in data_points:
        attr_key = []
        attr_keys = list(data_point.attributes.keys())
        attr_keys.sort()
        for key in attr_keys:
            attr_key.append(f"[{key}:{data_point.attributes[key]}]")
        attr_key.sort()

        keys[metric.name + ("".join(attr_key))] = data_point.value
    
    assert len(keys) == 2
    assert keys["some_gauge"] == 1
    assert keys["some_gauge[f1:hello]"] == 1.5

    c1 = CollectedMetrics.from_scheme("""
        some_gauge = 1
        some_gauge[f1:hello] = 1.5
        """ )
    c2 = CollectedMetrics.from_metrics_data( metrics_data )

FULL_LOG_MESSAGE = """===== EXPECTED SCHEME =====
some_gauge = 1.0
some_gauge[f1:hello] = 1.5

===== FOUND SCHEME =====
some_gauge = 1
some_gauge[f1:hello] = 1.4

===== REASON =====
Wrong value for metric 'some_gauge[f1:hello]', with expected value 1.5, found 1.4 (distance 0.10000000000000009 > 0)"""

@using_test_config
def test_metrics_log_using_test_tools (capsys):
    meter = get_meter("tests")
    gauge = meter.create_gauge("some_gauge", description="Some example gauge")

    gauge.set(1, {  })
    gauge.set(1.4, { "f1": "hello" })

    assert not CollectedMetrics.verify_scheme("""
        some_gauge = 1
        some_gauge[f1:hello] = 1.5
        """, verbosity = MetricsTestVerbosity.FULL_LOG)

    assert capsys.readouterr().out.strip() == FULL_LOG_MESSAGE
    
    gauge.set(1, {  })
    gauge.set(1.4, { "f1": "hello" })

    assert not CollectedMetrics.verify_scheme("""
        some_gauge = 1
        some_gauge[f1:hello] = 1.5
        """, verbosity = MetricsTestVerbosity.SIMPLE_ERROR)

    assert capsys.readouterr().out.strip() == FULL_LOG_MESSAGE.splitlines()[-1]
    gauge.set(1, {  })
    gauge.set(1.4, { "f1": "hello" })

    assert not CollectedMetrics.verify_scheme("""
        some_gauge = 1
        some_gauge[f1:hello] = 1.5
        """, verbosity = MetricsTestVerbosity.NONE)

    assert capsys.readouterr().out == ""
    gauge.set(1, {  })
    gauge.set(1.4, { "f1": "hello" })

    assert CollectedMetrics.verify_scheme("""
        some_gauge = 1
        some_gauge[f1:hello] = 1.5
        """, verbosity = MetricsTestVerbosity.FULL_LOG, tolerance=0.15)

@using_test_config
def test_some_metrics ():
    meter = get_meter("tests")
    gauge1 = meter.create_gauge("gauge1", description="Some example gauge")
    gauge2 = meter.create_gauge("gauge2", description="Some example gauge")

    gauge1.set(1)
    gauge2.set(1)

    assert CollectedMetrics.verify_scheme("""
        gauge1 = 1
        gauge2 = 1
    """)
@using_test_config
def test_missing_metrics (capsys):
    meter = get_meter("tests")
    gauge1 = meter.create_gauge("gauge1", description="Some example gauge")
    
    gauge1.set(1)

    assert not CollectedMetrics.verify_scheme("""
        gauge1 = 1
        gauge2 = 1
    """, verbosity = MetricsTestVerbosity.SIMPLE_ERROR)
    assert capsys.readouterr().out.strip() == "Missing metric 'gauge2', with expected value 1.0"
