import os
import pytest
from app.config import VONAGE_API_KEY, VONAGE_API_SECRET, VONAGE_NUMBER

def test_environment_variables():
    assert VONAGE_API_KEY is not None, "VONAGE_API_KEY is not set"
    assert VONAGE_API_SECRET is not None, "VONAGE_API_SECRET is not set"
    assert VONAGE_NUMBER is not None, "VONAGE_NUMBER is not set"

def test_invalid_environment_variables(monkeypatch):
    monkeypatch.setenv("VONAGE_API_KEY", "")
    monkeypatch.setenv("VONAGE_API_SECRET", "")
    monkeypatch.setenv("VONAGE_NUMBER", "")
    
    with pytest.raises(ValueError, match="Missing Vonage environment variables."):
        from app.config import VONAGE_API_KEY, VONAGE_API_SECRET, VONAGE_NUMBER
