import pytest
from app.enums import CallStatus

def test_call_status_enum():
    assert CallStatus.RECORDING.value == "recording"
    assert CallStatus.COMPLETED.value == "completed"
    assert CallStatus.FAILED.value == "failed"

    assert CallStatus("recording") == CallStatus.RECORDING
    assert CallStatus("completed") == CallStatus.COMPLETED
    assert CallStatus("failed") == CallStatus.FAILED

    with pytest.raises(ValueError):
        CallStatus("invalid_status")
