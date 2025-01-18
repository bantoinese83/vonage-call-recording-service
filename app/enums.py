# enums.py
from enum import Enum

class CallStatus(Enum):
    RECORDING = "recording"
    COMPLETED = "completed"
    FAILED = "failed"