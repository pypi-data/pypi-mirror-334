
import logging
import os

from unittest.mock import patch, Mock

import pytest

from telemetry import configure, configure_from_env
from telemetry.config import TelemetryConfigException, TestConfig as _TestConfig
from telemetry.config import BaseConfig, HttpConfig, \
    ENV_CONFIG_TYPE, ENV_HTTP_ENDPOINT, ENV_HTTP_LOGS_SUFFIX, \
    ENV_HTTP_METRICS_SUFFIX, ENV_HTTP_TRACES_SUFFIX, \
    Resource, SERVICE_NAME, ENV_CONFIG_LOGLEVEL, ENV_HTTP_FORCE_SLASH, \
    ENV_HTTP_LOGS_ENDPOINT, ENV_HTTP_METRICS_ENDPOINT, ENV_HTTP_TRACES_ENDPOINT

@patch("telemetry.metrics.configure_test")
@patch("telemetry.traces.configure_test")
@patch("telemetry.logging.configure_test")
def test_configure_test_config (logging_test: Mock, traces_test: Mock, metrics_test: Mock):
    config = _TestConfig()
    configure( config )

    logging_test.assert_called_once_with(config)
    traces_test.assert_called_once_with(config)
    metrics_test.assert_called_once_with(config)

@patch("telemetry.metrics.configure_http")
@patch("telemetry.traces.configure_http")
@patch("telemetry.logging.configure_http")
def test_configure_http_config (logging_http: Mock, traces_http: Mock, metrics_http: Mock):
    config = HttpConfig("http://localhost:4318")
    configure( config )

    logging_http.assert_called_once_with(config)
    traces_http.assert_called_once_with(config)
    metrics_http.assert_called_once_with(config)

    assert config.metrics_endpoint == "http://localhost:4318/v1/metrics"
    config.metrics_endpoint = "http://localhost:4319"
    assert config.metrics_endpoint == "http://localhost:4319"
    assert config.traces_endpoint == "http://localhost:4318/v1/traces"
    config.traces_endpoint = "http://localhost:4320"
    assert config.traces_endpoint == "http://localhost:4320"
    assert config.logs_endpoint == "http://localhost:4318/v1/logs"
    config.logs_endpoint = "http://localhost:4320"
    assert config.logs_endpoint == "http://localhost:4320"

def test_configure_http_config_no_setup ():
    config = HttpConfig()

    with pytest.raises( TelemetryConfigException, match="Expected the endpoint parameter to be set as the 'metrics_endpoint' variable wasn't set." ):
        config.metrics_endpoint
    with pytest.raises( TelemetryConfigException, match="Expected the endpoint parameter to be set as the 'traces_endpoint' variable wasn't set." ):
        config.traces_endpoint
    with pytest.raises( TelemetryConfigException, match="Expected the endpoint parameter to be set as the 'logs_endpoint' variable wasn't set." ):
        config.logs_endpoint

def create_obj (cls, args = [], kwargs = {}, fields = {}):
    obj = cls(*args, **kwargs)

    for key in fields:
        setattr(obj, key, fields[key])
def check_obj (a, b):
    assert dir(a) == dir(b)

    for x in dir(a):
        if "__" in x: continue
        assert getattr(a, x) == getattr(b, x)

@patch("telemetry.configure")
def test_from_env (configure: Mock, capsys):
    TESTS = []

    TESTS.append((
        None,
        {  }
    ))
    TESTS.append((
        _TestConfig(),
        { ENV_CONFIG_TYPE: "TEST" }
    ))
    for key in [ "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG" ]:
        tconfig = _TestConfig()
        tconfig.loglevel = getattr(logging, key)
        TESTS.append((tconfig, { ENV_CONFIG_TYPE: "TEST", ENV_CONFIG_LOGLEVEL: key }))
    TESTS.append((None, { ENV_CONFIG_TYPE: "TEST", ENV_CONFIG_LOGLEVEL: "<unknown>" }))
    tconfig = _TestConfig()
    tconfig.resource = Resource({ SERVICE_NAME: "some_service" })
    TESTS.append((
        tconfig,
        { ENV_CONFIG_TYPE: "TEST", "TELEMETRY_RESOURCE_SERVICE_NAME": "some_service" }
    ))
    TESTS.append((
        None,
        { ENV_CONFIG_TYPE: "HTTP" }
    ))
    config = HttpConfig("")
    config.logs_endpoint = "LOGS"
    config.metrics_endpoint = "METRICS"
    config.traces_endpoint = "TRACES"
    TESTS.append((
        config,
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_METRICS_ENDPOINT: "METRICS",
          ENV_HTTP_TRACES_ENDPOINT: "TRACES", ENV_HTTP_LOGS_ENDPOINT: "LOGS" }
    ))
    TESTS.append((
        None,
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_METRICS_ENDPOINT: "METRICS",
          ENV_HTTP_TRACES_ENDPOINT: "TRACES" }
    ))
    config = HttpConfig("http://localhost:4318")
    config.logs_endpoint = "LOGS"
    TESTS.append((
        config,
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318",
         ENV_HTTP_LOGS_ENDPOINT: "LOGS" }
    ))
    TESTS.append((
        HttpConfig( "http://localhost:4318/", True ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318/", ENV_HTTP_FORCE_SLASH: "TRUE" }
    ))
    TESTS.append((
        HttpConfig( "http://localhost:4318" ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318/", ENV_HTTP_FORCE_SLASH: "FALSE" },
        "WARNING, the ending '/' will be removed by default.\n"
    ))
    TESTS.append((
        HttpConfig( "http://localhost:4318" ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318/" },
        "WARNING, the ending '/' will be removed by default.\n"
    ))
    TESTS.append((
        None,
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318/", ENV_HTTP_FORCE_SLASH: "WRONG" }
    ))
    TESTS.append((
        HttpConfig( "http://localhost:4318" ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318" }
    ))
    TESTS.append((
        create_obj( HttpConfig, [ "http://localhost:4318" ], {}, { "suffix_traces": "/v2/traces" } ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318", ENV_HTTP_TRACES_SUFFIX: "/v2/traces" }
    ))
    TESTS.append((
        create_obj( HttpConfig, [ "http://localhost:4318" ], {}, { "suffix_metrics": "/v2/traces" } ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318", ENV_HTTP_METRICS_SUFFIX: "/v2/traces" }
    ))
    TESTS.append((
        create_obj( HttpConfig, [ "http://localhost:4318" ], {}, { "suffix_logs": "/v2/traces" } ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318", ENV_HTTP_LOGS_SUFFIX: "/v2/traces" }
    ))
    result = None
    for expects, envs, *args in TESTS:
        try:
            for key in envs.keys():
                os.environ.update([ (key, envs[key]) ])
            
            result = BaseConfig.from_env()

            check_obj(expects, result)
        except Exception as e:
            assert expects is None, f"{envs} {e} {expects}"
        finally:
            for key in envs.keys():
                os.environ.pop(key)
        if len(args) == 1:
            assert capsys.readouterr().out == args[0]
        else:
            assert capsys.readouterr().out == ""
        
        try:
            for key in envs.keys():
                os.environ.update([ (key, envs[key]) ])
            
            configure.reset_mock()
            configure_from_env()
            configure.assert_called_once()
            objs = configure.call_args_list[0]
            assert len(objs.args) == 1

            check_obj(expects, objs.args[0])
        except Exception as e:
            assert expects is None
        finally:
            for key in envs.keys():
                os.environ.pop(key)
        if len(args) == 1:
            assert capsys.readouterr().out == args[0]
        else:
            assert capsys.readouterr().out == ""
