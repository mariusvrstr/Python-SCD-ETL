from src.data_access.database.stage_repository import StageRepository
from src.data_access.database.master_repository import MasterRepository

class SCDService():
    context = None
    stage_repo = None
    master_repo = None

    def __init__(self, context) -> None:
        self.context = context
        self.stage_repo = StageRepository(context)
        self.master_repo = MasterRepository(context)

    def pre_processing(self, client_account_number):

        pass


    def process_staged_records(self):
        batches = self.stage_repo.get_ready_batches()

        #TODO: Process in multiple threads
        for batch in batches:
            self.pre_processing(batch.client_account)

            # for


        pass







