
import enum
from typing import Dict, List, Tuple, Type

from opentelemetry import metrics
from opentelemetry.metrics import get_meter
from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as GRPCExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as HTTPExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, InMemoryMetricReader

from telemetry.config import TestConfig, HttpConfig

#################
# CONFIGURATION #
#################

_TEST_READER = InMemoryMetricReader()

def _configure (resource, endpoint: str, exporter: "Type[GRPCExporter] | Type[HTTPExporter]"):
    exporter = exporter( endpoint )
    reader   = PeriodicExportingMetricReader( exporter )

    provider = MeterProvider(resource=resource, metric_readers=[reader])

    metrics.set_meter_provider(provider)

def configure_http (config: "HttpConfig"):
    _configure(config.resource, config.metrics_endpoint, HTTPExporter)

def get_test_reader ():
    return _TEST_READER
def configure_test (config: "TestConfig"):
    provider = MeterProvider(resource=config.resource, metric_readers=[_TEST_READER])

    metrics.set_meter_provider(provider)

#################
#### TESTING ####
#################

class MetricsTestVerbosity(enum.Enum):
    NONE = 0
    SIMPLE_ERROR = 1
    FULL_LOG = 2

class MetricResult:
    name  : str
    attr  : List[Tuple[str, str]]
    value : float

    def __init__(self, name: str, attr: Dict[str, str], value: float):
        self.name = name
        self.attr = []

        for key in attr.keys():
            self.attr.append((key, attr[key]))
        
        self.attr.sort()
        self.value = value

    def as_scheme_field (self):
        attrs = []

        for key, tar in self.attr:
            attrs.append(f"[{key}:{tar}]")

        attr = "".join(attrs)

        return f"{self.name}{attr}"
    def as_scheme (self):
        return f"{self.as_scheme_field()} = {self.value}"
    def is_less_than (self, name: str, attr: List[Tuple[str, str]]):
        if self.name != name:
            return self.name < name
        return self.attr < attr
    def __lt__ (self, other: "MetricResult"):
        return self.is_less_than(other.name, other.attr)

class CollectedMetrics:
    metrics: List[MetricResult]

    def get_metric (self, name: str, attrs: List[Tuple[str, str]]) -> "MetricResult | None":
        left  = -1
        right = len(self.metrics)

        while right - left > 1:
            mid = (left + right) >> 1

            if self.metrics[mid].is_less_than(name, attrs):
                left = mid
            else:
                right = mid

        if right == len(self.metrics) or self.metrics[right].name != name or self.metrics[right].attr != attrs:
            return None
        return self.metrics[right]

    def includes (self, other: "CollectedMetrics", tolerance: float = 0) -> "Tuple[bool, str | None]":
        for metric in other.metrics:
            local = self.get_metric( metric.name, metric.attr )
            if local is None:
                return False, f"Missing metric '{metric.as_scheme_field()}', with expected value {metric.value}"
            
            dist = abs(local.value - metric.value)
            if dist > tolerance:
                return False, f"Wrong value for metric '{metric.as_scheme_field()}', with expected value {metric.value}, found {local.value} (distance {dist} > {tolerance})"
        
        return True, None

    def as_scheme (self):
        self.metrics.sort()
        
        lines = []

        for metric in self.metrics:
            lines.append( metric.as_scheme() )
        
        return "\n".join(lines)

    @staticmethod
    def from_scheme (scheme: str):
        lines = scheme.splitlines()

        collected = CollectedMetrics()
        collected.metrics = []

        for line in lines:
            line = line.strip()
            if len(line) == 0: continue

            params, value = line.split("=")
            params = params.strip()
            value = value.strip()
            value = float(value)

            params = params.split("[")

            name = params[0].strip()
            args = {}

            for param in params[1:]:
                param = param.strip()
                param = param[:-1]

                key, tar = param.split(":")
                key = key.strip()
                tar = tar.strip()

                args[key] = tar
            
            metric = MetricResult(name, args, value)

            collected.metrics.append(metric)

        return collected
    @staticmethod
    def from_reader ():
        metrics_data = _TEST_READER.get_metrics_data()

        return CollectedMetrics.from_metrics_data(metrics_data)
    @staticmethod
    def from_metrics_data (metrics_data):
        resource_metrics = metrics_data.resource_metrics

        collected = CollectedMetrics()
        collected.metrics = []

        for resource_metric in resource_metrics:
            for scope_metric in resource_metric.scope_metrics:
                for metric in scope_metric.metrics:
                    for data_point in metric.data.data_points:
                        name, attr, value = metric.name, data_point.attributes, data_point.value
                        metric_result = MetricResult(name, attr, value)

                        collected.metrics.append(metric_result)

        return collected

    @staticmethod
    def verify_scheme (scheme: str, tolerance: float = 0, verbosity: MetricsTestVerbosity = MetricsTestVerbosity.NONE) -> bool:
        expects = CollectedMetrics.from_scheme(scheme)
        get_met = CollectedMetrics.from_reader()

        valid, err_message = get_met.includes(expects, tolerance)
        if valid:
            return True
        
        if verbosity == MetricsTestVerbosity.FULL_LOG:
            print("===== EXPECTED SCHEME =====")
            print(expects.as_scheme())
            print()

            print("===== FOUND SCHEME =====")
            print(get_met.as_scheme())
            print()

            print("===== REASON =====")
        if verbosity != MetricsTestVerbosity.NONE:
            print(err_message)
        
        return False
