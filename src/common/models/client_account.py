from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ClientAccount(BaseModel):
    id: int
    account_number: str
    last_updated: Optional[datetime]

    class Config:
        orm_mode=True
