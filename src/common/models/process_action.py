from enum import Enum

class ProcessAction(Enum):
    Unknown = "N/A"
    Add = "Add"
    Unchanged = "Unchanged"
    Append = "Append"
    Merge = "Merge"
    Replace = "Replace"
