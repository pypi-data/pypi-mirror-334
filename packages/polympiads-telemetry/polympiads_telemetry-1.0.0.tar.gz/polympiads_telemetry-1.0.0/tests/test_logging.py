
import re
import logging
from unittest.mock import Mock, patch

import pytest

from telemetry import using_test_config
from telemetry.config import HttpConfig
from telemetry.config import TestConfig as _TestConfig
from telemetry.logging import LogTestVerbosity, LoggingHandler, VirtualLogRecords, configure_http, configure_test, get_test_handler, set_test_handler
from telemetry.logging import TestLoggingHandler as _TestLoggingHandler

@patch("telemetry.logging.configure")
def test_configure_test (configure: Mock):
    conf = _TestConfig()
    configure_test( conf )
    
    configure.assert_called_once_with(conf, _TestLoggingHandler)
@patch("telemetry.logging.configure")
@patch("telemetry.logging.HttpExporter")
@patch("telemetry.logging.BatchLogRecordProcessor")
def test_configure_http (batch_log_record: Mock, http_exporter: Mock, configure: Mock):
    provider = Mock()
    configure.return_value = provider
    provider.add_log_record_processor = Mock()

    batch = batch_log_record.return_value = Mock()
    http  = http_exporter.return_value = Mock()

    conf = HttpConfig("http://localhost:4318")
    configure_http(conf)

    http_exporter.assert_called_once_with( endpoint=conf.logs_endpoint )
    batch_log_record.assert_called_once_with( http )
    provider.add_log_record_processor.assert_called_once_with( batch )

    configure.assert_called_once_with(conf, LoggingHandler)

def test_set_test_handler ():
    saved_handler = get_test_handler()
    set_test_handler( "handler" )
    assert get_test_handler() == "handler"
    set_test_handler(saved_handler)
    assert get_test_handler() is saved_handler

@patch("telemetry.logging.set_test_handler")
@patch("telemetry.logging.set_logger_provider")
@patch("telemetry.logging.LoggerProvider")
@patch("telemetry.logging.TestLoggingHandler")
@patch("logging.getLogger")
def test_configure_test_internal (
            get_logger: Mock, test_logging_handler: Mock,
            logger_provider: Mock, set_logger_provider: Mock,
            set_test_handler: Mock
        ):
    config = _TestConfig()
    provider = logger_provider.return_value = Mock()
    handler  = test_logging_handler.return_value = Mock()
    
    logger = get_logger.return_value = Mock()
    logger.setLevel = Mock()
    logger.addHandler = Mock()
    configure_test(config)

    logger_provider.assert_called_once_with( resource=config.resource )
    set_logger_provider.assert_called_once_with( provider )

    test_logging_handler.assert_called_once_with( config.loglevel, provider )
    logger.setLevel.assert_called_once_with( config.loglevel )
    logger.addHandler.assert_called_once_with( handler )
    set_test_handler.assert_called_once_with( handler )

@patch("telemetry.logging.set_test_handler")
@patch("telemetry.logging.set_logger_provider")
@patch("telemetry.logging.LoggerProvider")
@patch("telemetry.logging.LoggingHandler")
@patch("logging.getLogger")
@patch("telemetry.logging.HttpExporter")
@patch("telemetry.logging.BatchLogRecordProcessor")
def test_configure_http_internal (
            batch_processor: Mock, http_exporter: Mock,
            get_logger: Mock, logging_handler: Mock,
            logger_provider: Mock, set_logger_provider: Mock,
            set_test_handler: Mock
        ):
    config = HttpConfig( "http://localhost:4318" )
    config.formatter = Mock()

    provider = logger_provider.return_value = Mock()
    handler  = logging_handler.return_value = Mock()
    
    handler.setFormatter = Mock()

    http = http_exporter.return_value = Mock()
    batch = batch_processor.return_value = Mock()
    provider.add_log_record_processor = Mock()
    
    logger = get_logger.return_value = Mock()
    logger.setLevel = Mock()
    logger.addHandler = Mock()
    configure_http(config)

    logger_provider.assert_called_once_with( resource=config.resource )
    set_logger_provider.assert_called_once_with( provider )
    handler.setFormatter.assert_called_once_with( config.formatter )

    logging_handler.assert_called_once_with( config.loglevel, provider )
    logger.setLevel.assert_called_once_with( config.loglevel )
    logger.addHandler.assert_called_once_with( handler )
    set_test_handler.assert_not_called()

    provider.add_log_record_processor.assert_called_once_with( batch )
    batch_processor.assert_called_once_with( http )
    http_exporter.assert_called_once_with( endpoint = config.logs_endpoint )

@using_test_config
def test_check_logs_manually ():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)

    re = _TestConfig()
    re.method = "GET"
    re.path = "/path"
    logger.critical ( "Some critical message", extra={"param":1, "request": re} )
    logger.error    ( "Some error message",    extra={"param":2})
    logger.warning  ( "Some warning message"  )
    logger.info     ( "Some info message"     )
    logger.debug    ( "Some debug message"    )

    handler = get_test_handler()
    records = handler.get_sent_records()
    handler.clear()

    def _check (a, b):
        for key in b.keys():
            if a[key] != b[key]:
                return False
        return True

    assert len(records) == 3
    assert records[0].body == "Some critical message" and records[0].severity_text == "CRITICAL" and _check(records[0].attributes, {"param":1, "request": "GET /path"})
    assert records[1].body == "Some error message"    and records[1].severity_text == "ERROR"    and _check(records[1].attributes, {"param":2})
    assert records[2].body == "Some warning message"  and records[2].severity_text == "WARN"     and _check(records[2].attributes, {})

@using_test_config
def test_check_logs_automatic ():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)

    re = _TestConfig()
    re.method = "GET"
    re.path = "/path"
    logger.critical ( "Some critical message", extra={"param":1, "request": re} )
    logger.error    ( "Some error message",    extra={"param":2})
    logger.warning  ( "Some warning message"  )
    logger.info     ( "Some info message"     )
    logger.debug    ( "Some debug message"    )

    assert VirtualLogRecords.verify_from_scheme("""
    CRITICAL "Some critical message" [param:1][request:GET /path]
    ERROR    "Some error message"    [param:2]
    WARN     "Some warning message"
    """)

@using_test_config
def test_check_logs_automatic_wrong_number_of_logs_but_verb_none (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)

    re = _TestConfig()
    re.method = "GET"
    re.path = "/path"
    logger.critical ( "Some critical message", extra={"param":1, "request": re} )
    logger.error    ( "Some error message",    extra={"param":2})

    assert not VirtualLogRecords.verify_from_scheme("""
    CRITICAL "Some critical message" [param:1][request:GET /path]
    ERROR    "Some error message"    [param:2]
    WARN     "Some warning message"
    """)
    assert get_test_handler().get_sent_records() == []
    assert capsys.readouterr().out == ""

# For the love of god, never touch this regular expression
#  number of hours wasted = 1
# Also if you have an issue, DO NOT REMOVE the space after the warning log
RE_CHECK_LOGS_AUTOMATIC_WRONG_NUM_OF_LOGS = re.compile( '''===== EXPECTED =====
CRITICAL "Some critical message" \\[param:1\\]\\[request:GET \\/path\\]
ERROR "Some error message" \\[param:2\\]
WARN "Some warning message" 

===== FOUND =====
CRITICAL "Some critical message" \\[param:1\\]\\[request:GET \\/path\\](\\[.*:.*\\])*
ERROR "Some error message" \\[param:2\\](\\[.*:.*\\])*

Not the same number of logs on both sides\\.'''.replace("\n", "\\n") )

@using_test_config
def test_check_logs_automatic_wrong_number_of_logs (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)

    re = _TestConfig()
    re.method = "GET"
    re.path = "/path"
    logger.critical ( "Some critical message", extra={"param":1, "request": re} )
    logger.error    ( "Some error message",    extra={"param":2})

    assert not VirtualLogRecords.verify_from_scheme("""
    CRITICAL "Some critical message" [param:1][request:GET /path]
    ERROR    "Some error message"    [param:2]
    WARN     "Some warning message"
    """, verbosity=LogTestVerbosity.FULL)
    assert RE_CHECK_LOGS_AUTOMATIC_WRONG_NUM_OF_LOGS.match( capsys.readouterr().out.strip() ) is not None
@using_test_config
def test_check_logs_automatic_wrong_message (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)
    logger.critical( "Some critical message", extra={"param":1} )
    assert not VirtualLogRecords.verify_from_scheme("""
    CRITICAL "Some wrong critical message" [param:1]
    """, verbosity=LogTestVerbosity.ONLY_ERROR)
    assert capsys.readouterr().out.strip() == 'Two messages differ, found "Some critical message", expected "Some wrong critical message"'
@using_test_config
def test_check_logs_automatic_wrong_loglevel (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)
    logger.critical( "Some critical message", extra={"param":1} )
    assert not VirtualLogRecords.verify_from_scheme("""
    ERROR "Some critical message" [param:1]
    """, verbosity=LogTestVerbosity.ONLY_ERROR)
    assert capsys.readouterr().out.strip() == 'The log level differs on messages "Some critical message", found CRITICAL expected ERROR'
@using_test_config
def test_check_logs_automatic_missing_param (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)
    logger.critical( "Some critical message", extra={"param2":1} )
    assert not VirtualLogRecords.verify_from_scheme("""
    CRITICAL "Some critical message" [param:2]
    """, verbosity=LogTestVerbosity.ONLY_ERROR)
    assert capsys.readouterr().out.strip() == 'The log with message "Some critical message" is missing the attribute "param", expected value "2"'
@using_test_config
def test_check_logs_automatic_wrong_param (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)
    logger.critical( "Some critical message", extra={"param":1} )
    assert not VirtualLogRecords.verify_from_scheme("""
    CRITICAL "Some critical message" [param:2]
    """, verbosity=LogTestVerbosity.ONLY_ERROR)
    assert capsys.readouterr().out.strip() == 'The log attribute "param" differs on message "Some critical message", expected "2", got "1"'
@using_test_config
def test_check_logs_automatic_simpler_format (capsys):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.WARNING)
    logger.critical( "Some critical message" )
    assert VirtualLogRecords.verify_from_scheme("""
    CRITICAL Some critical message
    """, verbosity=LogTestVerbosity.ONLY_ERROR)
@using_test_config
def test_check_logs_automatic_wrong_format (capsys):
    with pytest.raises(AssertionError, match="Missing closing \" in line 'CRITICAL \"F'"):
        VirtualLogRecords.from_scheme("CRITICAL \"F")