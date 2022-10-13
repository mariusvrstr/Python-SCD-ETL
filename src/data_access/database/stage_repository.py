import ctypes
import typing

from datetime import datetime
from src.data_access.database.models.database_models import StageRecordEntity, StageBatchEntity
from src.application.models.stage_batch import StageBatch
from src.application.models.stage_record import StageRecord
from src.application.models.file_item import FileItem
from src.application.models.batch_status import BatchStatus
from src.data_access.database.common.repository_base import RepositoryBase
from sqlalchemy.sql import select

class StageRepository(RepositoryBase):

    def __init__(self, context) -> None:
        super().__init__(context, StageRecordEntity, StageRecord)

    def get_ready_batches(self):
        batches = self.context.query(StageBatchEntity).filter(
            StageBatchEntity.batch_status == BatchStatus.Ready.value)

        items = self.map_all(StageBatch, batches)
        return items

    def get_stage_batch(self, client_account, file_hash) -> StageBatch:
        batch = self.context.query(StageBatchEntity).filter(
            StageBatchEntity.client_account == client_account and StageBatchEntity.file_hash == file_hash and StageBatchEntity.batch_status != BatchStatus.Deleted.value).first() 
        
        mapped = self.map(StageBatch, batch)
        return mapped

    def add_stage_batch(self, client_account, filename, file_hash):
        batch = StageBatchEntity().create(client_account, filename, file_hash)
        self.context.add(batch)
        self.sync(batch)

        mapped = self.map(StageBatch, batch)
        return mapped

    def add_stage_record(self, file_item: FileItem, batch_id: int) -> StageRecord:
        record = StageRecordEntity().create(
            file_item.effective_date, file_item.external_refrence, file_item.company_name, 
            file_item.amount, file_item.term.value, batch_id)
        self.add(record)
        self.sync(record)

        mapped = self.map(StageRecord, record)
        return mapped

    def complete_batch(self, batch_id, success_count: int, failure_count: int, error_threshold = 0.0):
        batch = self.context.get(StageBatchEntity, batch_id)

        if success_count == 0 or (failure_count > 0 and ((success_count/failure_count) > error_threshold)):
            batch.batch_status = BatchStatus.Error.value
        else:
            batch.end_date = datetime.now()
            batch.batch_status = BatchStatus.Ready.value

        batch.success_count = success_count
        batch.failure_count = failure_count

        self.sync()
        mapped = self.map(StageBatch, batch)
        return mapped
