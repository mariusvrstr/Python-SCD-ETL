from enum import Enum

# Column in the Excel File
class SCDAction(Enum):
    Undefined = 0
    NoChanges = 1
    Add = 2
    Append = 3
    Insert = 4


