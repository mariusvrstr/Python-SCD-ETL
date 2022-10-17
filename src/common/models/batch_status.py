from enum import Enum

class BatchStatus(Enum):
    Undefined = "N/A"
    InProgress = "In Progress"
    Ready = "Ready"
    Complete = "Complete"
    Error = "Error"
    Deleted = "Deleted"


