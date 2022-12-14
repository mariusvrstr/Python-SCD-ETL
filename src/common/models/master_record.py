from datetime import datetime
from pydantic import BaseModel
from src.common.models.term import Term
from typing import Optional

class MasterRecord(BaseModel):
    id: int
    external_reference: str
    company_name: str
    amount: Optional[float]
    term: Optional[Term]
    from_date: datetime
    to_date: Optional[datetime]
    last_updated: datetime
    is_deleted: bool = False
    is_placeholder: bool = False
    # Has changes should be one level higher out of SCD 1:1 with relationship
    has_changes: bool = False
    batch_id: int
    client_account_id: int

    class Config:
        orm_mode=True
