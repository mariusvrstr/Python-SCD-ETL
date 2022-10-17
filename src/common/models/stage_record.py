from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.common.models.process_action import ProcessAction
from src.common.models.process_status import ProcessStatus
from src.common.models.term import Term

class StageRecord(BaseModel):
    id: int
    effective_date: datetime
    insert_date: datetime
    external_reference: str
    company_name: str
    amount: Optional[float]
    term: Optional[Term]
    process_status: ProcessStatus = ProcessStatus.Unprocessed
    process_action: ProcessAction = ProcessAction.Unknown
    batch_id: int

    class Config:
        orm_mode=True