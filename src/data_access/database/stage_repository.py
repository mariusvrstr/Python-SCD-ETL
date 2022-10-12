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

    def get_stage_batch(self, client_account, file_hash) -> StageBatch:
        batch = self.context.query(StageBatchEntity).filter(
            StageBatchEntity.client_account == client_account and StageBatchEntity.file_hash == file_hash and StageBatchEntity.batch_status != BatchStatus.Deleted.value).first() 
        
        mapped = self.map_to_business_batch(batch)
        return mapped

    def add_stage_batch(self, client_account, filename, file_hash):
        new_batch = StageBatchEntity().create(client_account, filename, file_hash)
        self.context.add(new_batch)
        self.sync(new_batch)

        mapped = self.map_to_business_batch(new_batch)
        return mapped

    def add_stage_record(self, file_item: FileItem, batch_id: int) -> StageRecord:
        new_stage_record = StageRecordEntity().create(
            file_item.effective_date, file_item.external_refrence, file_item.company_name, file_item.amount, file_item.status.value, batch_id)

        self.add(new_stage_record)
        return self.map_to_business(new_stage_record)

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
        return self.map_to_business_batch(batch)

    '''
    ========================================
    Mappers TODO: Replace with a auto mapper
    ========================================
    '''
    def map_to_business(self, db_object: StageRecordEntity) -> StageRecord:
        if (db_object is None):
            return None

        mapped = StageRecord().create(
            db_object.effective_date, db_object.insert_date, db_object.external_reference, db_object.amount, db_object.status, db_object.id)
        return mapped

    def map_to_database(self, bus_object) -> StageRecordEntity:
        raise ValueError('Map to database is not used')

    def map_to_business_batch(self, db_object: StageBatchEntity) -> StageBatch:
        if (db_object is None):
            return None
            
        mapped = StageBatch().create(db_object.client_account, db_object.start_date, db_object.end_date, db_object.file_hash, 
            db_object.filename, db_object.success_count, db_object.failure_count,
            db_object.batch_status, db_object.id)
        return mapped