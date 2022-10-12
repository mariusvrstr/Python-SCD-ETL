from ast import Index
from datetime import datetime
from tokenize import String
from unicodedata import name
from src.data_access.database.common.database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UniqueConstraint
from src.application.models.batch_status import BatchStatus

class StageBatchEntity(Base):
    __tablename__ = 'StageBatch'
    id = Column(Integer, primary_key=True, index=True)
    client_account = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    filename = Column(String)
    file_hash = Column(String)
    success_count = Column(Integer)
    failure_count = Column(Integer)
    batch_status = Column(String)
    
    # Foreign Key - Many Side Opposed to One
    records = relationship('StageRecordEntity', back_populates='')

    def create(self, client_account, filename, file_hash, id = None):
        self.id = id
        self.client_account = client_account
        self.start_date = datetime.now()
        self.success_count = 0
        self.failure_count = 0
        self.file_hash = file_hash
        self.filename = filename
        self.batch_status = BatchStatus.InProgress.value

        return self

class StageRecordEntity(Base):
    __tablename__ = 'StageRecord'

    id = Column(Integer, primary_key=True, index=True)
    effective_date = Column(DateTime)
    insert_date = Column(DateTime)
    external_reference = Column(String)
    company_name = Column(String)
    amount = Column(Float)
    status = Column(String)

   # Foreign Key - One Side Oposed to Many
    batch_id = Column(Integer, ForeignKey('StageBatch.id'))

    # UniqueConstraint("batch_id", "external_reference", name="unique_debtor_batch")

    def create(self, effective_date, external_reference, company_name, amount, status, batch_id, id = None):
        self.id = id
        self.effective_date = effective_date
        self.insert_date = datetime.now()
        self.external_reference = external_reference
        self.company_name = company_name
        self.amount = amount
        self.status = status
        self.batch_id = batch_id

        return self

