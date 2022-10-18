import ctypes
from datetime import datetime
from operator import and_, or_
from src.common.models.process_action import ProcessAction
from src.common.models.process_status import ProcessStatus
from src.data_access.database.models.database_models import StageRecordEntity, StageBatchEntity
from src.common.models.stage_batch import StageBatch
from src.common.models.stage_record import StageRecord
from src.common.models.file_item import FileItem
from src.common.models.batch_status import BatchStatus
from src.data_access.database.common.repository_base import RepositoryBase
from sqlalchemy.sql import select

class StageRepository(RepositoryBase):

    def __init__(self, context) -> None:
        super().__init__(context, StageRecordEntity, StageRecord)

    def get_ready_batches(self, size:int = 50) -> ctypes.Array:
        batches = self.context.query(StageBatchEntity).filter(
            StageBatchEntity.batch_status == BatchStatus.Ready.value).order_by(StageBatchEntity.start_date).limit(size).all()

        return self.map_all(batches, StageBatch)

    def get_batched_stage_records(self, batch_id, process_status: ProcessStatus = ProcessStatus.Unprocessed, size: int = 20) -> ctypes.Array:
        records = self.context.query(StageRecordEntity).filter(
            StageRecordEntity.batch_id == batch_id,
            StageRecordEntity.process_status == process_status.value
        ).limit(size).all()
        
        return self.map_all(records)
        
    def get_stage_batch(self, file_hash, client_account = None) -> StageBatch:
        batch = None

        #TODO: The below is ugly need time to work out filtering usually do a (var = None or column = var) that combines below
        if (client_account is not None):
            batch = self.context.query(StageBatchEntity).filter(
                    StageBatchEntity.file_hash == file_hash,
                    StageBatchEntity.batch_status != BatchStatus.Deleted.value,
                    StageBatchEntity.client_account == client_account).one_or_none()
        else: 
            batch = self.context.query(StageBatchEntity).filter(
                    StageBatchEntity.file_hash == file_hash,
                    StageBatchEntity.batch_status == BatchStatus.InProgress.value).one_or_none()  

        return self.map(batch, StageBatch)

    def add_stage_batch(self, client_account, filename, file_hash):
        batch = StageBatchEntity().create(client_account, filename, file_hash)
        self.context.add(batch)
        self.sync(batch)

        return self.map(batch, StageBatch)

    def add_stage_record(self, file_item: FileItem, batch_id: int) -> StageRecord:
        record = StageRecordEntity().create(
            file_item.effective_date, file_item.external_refrence, file_item.company_name, 
            file_item.amount, file_item.term.value, batch_id)
        self.add(record)
        self.sync(record)

        return self.map(record)

    def finalize_batch_upload(self, batch_id, success_count: int, failure_count: int, error_threshold = 0.0):
        batch = self.context.get(StageBatchEntity, batch_id)

        if success_count == 0 or (failure_count > 0 and ((success_count/failure_count) > error_threshold)):
            batch.batch_status = BatchStatus.Error.value
        else:
            batch.end_date = datetime.now()
            batch.batch_status = BatchStatus.Ready.value

        batch.success_count = success_count
        batch.failure_count = failure_count

        self.sync()
        return self.map(batch, StageBatch)

    def complete_batch_process(self, id, batch_status: BatchStatus = BatchStatus.Complete):
        batch = self.context.get(StageBatchEntity, id)
        batch.batch_status = batch_status.value
        self.sync(batch)

    def complete_stage_record_process(self, id, process_status: ProcessStatus, process_action: ProcessAction):
        record = self.context.get(StageRecordEntity, id)
        record.process_status = process_status.value
        record.process_action = process_action.value
        self.sync(record)