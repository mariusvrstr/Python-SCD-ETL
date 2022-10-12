from enum import Enum

# Column in the Excel File
class RecordStatus(Enum):
    Undefined = 0
    Active = 1
    Inactive = 2
    Pending = 3


