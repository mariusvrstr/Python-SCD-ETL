from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.application.models.batch_status import BatchStatus

class StageBatch(BaseModel):
    id: int
    client_account: str
    start_date: datetime
    end_date: Optional[datetime]
    file_hash: str
    filename: str
    success_count: int = 0
    failure_count: int = 0
    batch_status: BatchStatus = BatchStatus.Undefined

    class Config:
        orm_mode=True
