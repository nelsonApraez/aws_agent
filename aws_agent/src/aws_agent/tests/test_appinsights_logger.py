import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import os
import logging
import pytest
from aws_agent.tools import appinsights_logger

def test_log_event(monkeypatch):
    logs = []
    class DummyHandler(logging.Handler):
        def emit(self, record):
            logs.append(record.getMessage())
    logger = logging.getLogger("app_insights")
    logger.handlers = []
    logger.addHandler(DummyHandler())
    monkeypatch.setattr(appinsights_logger, "logger", logger)
    appinsights_logger.log_event("test_type", {"foo": "bar"}, "sess", "inter", agent_name="TestAgent")
    assert any("TestAgent" in str(log) for log in logs)
