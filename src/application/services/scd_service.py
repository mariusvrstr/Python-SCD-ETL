from src.data_access.database.stage_repository import StageRepository
from src.data_access.database.master_repository import MasterRepository
from src.data_access.database.common.database import get_db_Session, engine

from src.application.models.process_status import ProcessStatus
from src.application.models.stage_record import StageRecord
from src.data_access.database.master_repository import MasterRepository
from src.data_access.database.stage_repository import StageRepository

class SCDService():
    context = None
    stage_repo = None
    master_repo = None

    def __init__(self, context) -> None:
        self.context = context

    def pre_processing(self, client_account_number):
        # Add placholder entries for entries that is older that the validity period of last insert
        pass

    def post_processing(self, client_account_number):
        pass


    def process_staged_records(self):
        stage_repo = StageRepository(self.context)
        master_repo = MasterRepository(self.context)
        batches = stage_repo.get_ready_batches()

        for batch in batches:
            
            try:
                client_account = master_repo.get_client_account(batch.client_account)
                if (client_account is None):
                    client_account = master_repo.add_client_account(batch.client_account)
                    self.context.commit()

                stage_records = stage_repo.get_batched_stage_records(batch.id, ProcessStatus.Unprocessed, 5)

                while len(stage_records) > 0:
                    self.context = get_db_Session()
                    stage_repo = StageRepository(self.context)
                    master_repo = MasterRepository(self.context)

                    while len(stage_records) > 0:
                        record = stage_records.pop()

                        try:
                            print(f'SCD THE STAGE RECORD ID [{record.id}]/ BATC [{batch.id}]')
                            # Should this be in a seperate indipendant contex?
                            update_action = master_repo.add_master_record(record, client_account.id)
                            stage_repo.complete_stage_record_process(record.id, ProcessStatus.Processed, update_action)

                        except Exception as ex:
                            # If one record fails it should not impact others from processing
                            print(f"Oops! {ex.__class__} occurred. Details: {ex}")
                            stage_repo.complete_stage_record_process(record.id, ProcessStatus.Failed)

                    self.context.commit()
                    stage_records = stage_repo.get_batched_stage_records(batch.id, ProcessStatus.Unprocessed, 5)   

                stage_repo.complete_batch_process(batch.id)
                self.context.commit()

            except Exception as ex:
                # If one batch fails it should not impact others from processing
                print(f"Oops! {ex.__class__} occurred. Details: {ex}")
                self.context.rollback()
         
            finally:
                self.context.close()
     




