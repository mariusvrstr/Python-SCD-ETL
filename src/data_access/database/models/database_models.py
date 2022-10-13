from ast import Index
from datetime import datetime
from tokenize import String
from unicodedata import name
from src.data_access.database.common.database import Base
from sqlalchemy.sql import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UniqueConstraint
from src.application.models.batch_status import BatchStatus
from src.application.models.process_status import ProcessStatus

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
    term = Column(String)
    process_status = Column(String)

    # Foreign Key - One Side Oposed to Many
    batch_id = Column(Integer, ForeignKey('StageBatch.id'))

    # UniqueConstraint("batch_id", "external_reference", name="unique_debtor_batch")

    def create(self, effective_date, external_reference, company_name, amount, term, batch_id, process_status = ProcessStatus.Unprocessed, id = None):
        self.id = id
        self.effective_date = effective_date
        self.insert_date = datetime.now()
        self.external_reference = external_reference
        self.company_name = company_name
        self.amount = amount
        self.term = term
        self.process_status = process_status.value
        self.batch_id = batch_id

        return self

class MasterRecordEntity(Base):
    __tablename__ = 'MasterRecord'
    id = Column(Integer, primary_key=True, index=True)
    external_reference = Column(String)
    company_name = Column(String)
    amount = Column(Float)
    term = Column(String)

    from_date = Column(DateTime)
    to_date = Column(DateTime)
    last_updated = Column(DateTime)
    is_deleted = Column(Boolean)
    # Has changes should be one level higher out of SCD 1:1 with relationship
    has_changes = Column(Boolean)
       
    # Foreign Key - One Side Oposed to Many
    batch_id = Column(Integer, ForeignKey('StageBatch.id'))
    client_account_id = Column(Integer, ForeignKey('ClientAccount.id'))

    def create(self, external_reference, company_name, amount, term, client_account_id, from_date, batch_id, is_placeholder = False, id = None):
        self.id = id
        self.external_reference = external_reference
        self.company_name = company_name
        self.amount = amount
        self.term = term
        self.client_account_id = client_account_id
        self.is_deleted = False
        self.is_placeholder = is_placeholder
        self.from_date = from_date
        self.to_date = null()
        self.last_updated = datetime.now()        
        self.has_changes = False
        self.batch_id = batch_id

        return self

class ClientAccountEntity(Base):
    __tablename__ = 'ClientAccount'
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String)
    last_updated = Column(DateTime)

    records = relationship('MasterRecordEntity', back_populates='')

    def create(self, account_number, id = None):
        self.id = id
        self.account_number = account_number
        self.last_updated = datetime.now()

        return self
