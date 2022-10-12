from enum import Enum

# Column in the Excel File
class BatchStatus(Enum):
    Undefined = "N/A"
    InProgress = "In Progress"
    Complete = "Complete"
    Error = "Error"
    Deleted = "Deleted"


