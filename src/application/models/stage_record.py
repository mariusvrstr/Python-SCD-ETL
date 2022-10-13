from datetime import datetime
from xmlrpc.client import Boolean
from pydantic import BaseModel
from typing import Optional
from src.application.models.term import Term

class StageRecord(BaseModel):
    id: int
    effective_date: datetime
    insert_date: datetime
    external_reference: str
    company_name: str
    amount: Optional[float]
    term: Optional[Term]
    is_processed: bool = False

    class Config:
        orm_mode=True