import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from fastapi.testclient import TestClient
from aws_agent.api import app

client = TestClient(app)

def test_run_agent_success(monkeypatch):
    class DummyResult:
        raw = "test output"
    def dummy_kickoff(self, inputs):
        return DummyResult()
    monkeypatch.setattr("aws_agent.crew.AwsAgent.crew", lambda self: type("Crew", (), {"kickoff": dummy_kickoff})())
    response = client.post("/run-agent", json={"topic": "test topic", "session_id": "test_session"})
    assert response.status_code == 200
    assert "result" in response.json()

def test_run_agent_error(monkeypatch):
    def dummy_kickoff(self, inputs):
        raise Exception("fail")
    monkeypatch.setattr("aws_agent.crew.AwsAgent.crew", lambda self: type("Crew", (), {"kickoff": dummy_kickoff})())
    response = client.post("/run-agent", json={"topic": "test topic", "session_id": "test_session"})
    assert response.status_code == 200
    assert "error" in response.json()
