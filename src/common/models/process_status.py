from enum import Enum

class ProcessStatus(Enum):
    Unprocessed = "Unprocessed"
    Processed = "Processed"
    Failed = "Failed"
