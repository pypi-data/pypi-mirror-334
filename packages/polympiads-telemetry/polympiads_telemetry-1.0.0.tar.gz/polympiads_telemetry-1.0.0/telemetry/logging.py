
from typing import Dict, List, Type
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggingHandler as OpenTelemetryLoggingHandler
from opentelemetry.sdk._logs import LoggerProvider, LogRecord

from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as HttpExporter

from opentelemetry._logs import set_logger_provider

from telemetry.config import BaseConfig, HttpConfig, TestConfig

import logging

#################
# CONFIGURATION #
#################

class LoggingHandler (OpenTelemetryLoggingHandler):
    @staticmethod
    def _get_attributes(record: logging.LogRecord):
        attributes = OpenTelemetryLoggingHandler._get_attributes(record)
        if "request" in attributes:
            attributes["request"] = f'{attributes["request"].method} {attributes["request"].path}'
        return attributes

class TestLoggingHandler (LoggingHandler):
    records: List[LogRecord] = []

    def clear (self):
        self.records = []
    def get_sent_records (self):
        return self.records

    def emit(self, record):
        record = self._translate(record)

        self.records.append(record)

_TEST_HANDLER = None
def get_test_handler () -> "TestLoggingHandler":
    return _TEST_HANDLER
def set_test_handler (handler: "TestLoggingHandler"):
    global _TEST_HANDLER
    _TEST_HANDLER = handler

def configure (config: BaseConfig, handler_class: "Type[LoggingHandler]" = LoggingHandler):
    logger_provider = LoggerProvider(
        resource=config.resource
    )
    set_logger_provider(logger_provider)

    handler = handler_class( config.loglevel, logger_provider )
    logging.getLogger().setLevel( config.loglevel )
    logging.getLogger().addHandler(handler)

    if config.formatter is not None:
        handler.setFormatter(config.formatter)

    if isinstance(config, TestConfig):
        set_test_handler(handler)

    return logger_provider

def configure_test (config: TestConfig):
    configure(config, TestLoggingHandler)
def configure_http (config: HttpConfig):
    logger_provider = configure(config, LoggingHandler)

    otlp_exporter = HttpExporter(endpoint=config.logs_endpoint)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

#################
#### TESTING ####
#################

class LogTestVerbosity:
    NONE = 0
    ONLY_ERROR = 1
    FULL = 2

class VirtualLog:
    loglevel   : str
    attributes : Dict[str, str]
    message    : str

class VirtualLogRecords:
    logs: List[VirtualLog]

    def __init__(self):
        self.logs = []

    def as_scheme (self):
        lines = []
        for log in self.logs:
            attrs = []
            for key in log.attributes.keys():
                attrs.append(f"[{key}:{log.attributes[key]}]")
            attrs_str = "".join(attrs)
            lines.append(f"{log.loglevel} \"{log.message}\" {attrs_str}")
        return "\n".join(lines)

    def includes_args_and_matches_with (self, other: "VirtualLogRecords"):
        if len(self.logs) != len(other.logs):
            return False, "Not the same number of logs on both sides."

        for log1, log2 in zip(self.logs, other.logs):
            if log1.message != log2.message:
                return False, f'Two messages differ, found "{log1.message}", expected "{log2.message}"'
            if log1.loglevel != log2.loglevel:
                return False, f'The log level differs on messages "{log1.message}", found {log1.loglevel} expected {log2.loglevel}'

            for key in log2.attributes.keys():
                if key not in log1.attributes:
                    return False, f'The log with message "{log1.message}" is missing the attribute "{key}", expected value "{log2.attributes[key]}"'
                if str(log1.attributes[key]) != str(log2.attributes[key]):
                    return False, f'The log attribute "{key}" differs on message "{log1.message}", expected "{str(log2.attributes[key])}", got "{str(log1.attributes[key])}"'
        
        return True, None

    @staticmethod
    def from_scheme (scheme: str):
        lines = scheme.splitlines()

        records = []
        for line in lines:
            line = line.strip()
            if line == "": continue

            loglevel, params = line.split(" ", 1)
            params = params.strip()

            if params[0] == '"':
                params = params[1:]

                offset = params.find('"')
                if offset == -1:
                    assert False, f"Missing closing \" in line '{line}'"
                else:
                    message = params[:offset]
                    params = params[offset + 1:]

                    words = ("".join(params.split("]"))).split("[")[1:]
                    attrs = {}
                    for word in words:
                        key, arg = word.split(":", 1)
                        attrs[key] = arg
            else:
                message = params
                attrs = {}

            record = VirtualLog()
            record.loglevel = loglevel
            record.message  = message
            record.attributes = attrs
            records.append(record)
        log_records = VirtualLogRecords()
        log_records.logs = records
        return log_records
    @staticmethod
    def from_records (records: List[LogRecord]):
        log_records = VirtualLogRecords()

        for record in records:
            log = VirtualLog()
            log.loglevel = record.severity_text
            log.attributes = record.attributes
            log.message = record.body

            log_records.logs.append(log)
        
        return log_records
    @staticmethod
    def from_handler (clear: bool = True):
        records = _TEST_HANDLER.get_sent_records()

        if clear:
            _TEST_HANDLER.clear()
            assert len(_TEST_HANDLER.get_sent_records()) == 0

        return VirtualLogRecords.from_records(records)

    @staticmethod
    def verify_from_scheme (scheme: str, clear: bool = True, verbosity = LogTestVerbosity.NONE):
        record_handler = VirtualLogRecords.from_handler(clear)
        record_scheme  = VirtualLogRecords.from_scheme(scheme)

        valid, message = record_handler.includes_args_and_matches_with(record_scheme)
        if valid:
            return True

        if verbosity == LogTestVerbosity.FULL:
            print("===== EXPECTED =====")
            print(record_scheme.as_scheme())
            print()
            print("===== FOUND =====")
            print(record_handler.as_scheme())
            print()
        if verbosity != LogTestVerbosity.NONE:
            print(message)
        return False
