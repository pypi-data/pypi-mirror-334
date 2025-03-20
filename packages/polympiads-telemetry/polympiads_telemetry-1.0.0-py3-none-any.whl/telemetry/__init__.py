
from functools import wraps
import os
import enum

import telemetry.metrics as metrics
import telemetry.traces  as traces
import telemetry.logging as _logging

from contextlib import contextmanager
from telemetry.config import *

def configure_from_env ():
    config = BaseConfig.from_env()

    configure(config)

def configure (config: BaseConfig):
    if isinstance(config, TestConfig):
        metrics.configure_test( config )
        traces .configure_test( config )
        
        _logging.configure_test( config )
    
    if isinstance(config, HttpConfig):
        metrics.configure_http( config )
        traces .configure_http( config )

        _logging.configure_http( config )

_TEST_CONFIGURED = False

def using_test_config (func):
    @wraps(func)
    def with_test_config (*args, **kwargs):
        global _TEST_CONFIGURED
        if not _TEST_CONFIGURED:
            _TEST_CONFIGURED = True

            configure( TestConfig() )
        
        return func(*args, **kwargs)

    return with_test_config
