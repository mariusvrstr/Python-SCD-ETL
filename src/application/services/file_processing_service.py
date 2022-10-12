from datetime import datetime
from xmlrpc.client import Boolean
import pandas as pd
import os
import hashlib

from src.application.models.file_headings import FileHeadings
from src.application.models.stage_batch import StageBatch
from src.application.models.file_item import FileItem
from src.data_access.database.stage_repository import StageRepository
from src.application.models.batch_status import BatchStatus

class FileProcessingService():
    context = None
    stage_repo = None

    def __init__(self, context) -> None:
        self.context = context
        self.stage_repo = StageRepository(context)

    def _get_file_hash(self, file_path):
        h = hashlib.sha1()

        with open(file_path,'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)
        
        return h.hexdigest()

    def process_item(self, item: FileItem, batch_id: int) -> Boolean:
        
        try:
            print(item.to_string())
            self.stage_repo.add_stage_record(item, batch_id)
            return True

        except Exception as ex:
            print(f"Oops! {ex.__class__} occurred. Details: {ex}") 
            return False

    def process_file(self, file_path) -> StageBatch:

        try:
            data = pd.read_excel(file_path)
            df = pd.DataFrame(data)

            client_account = df.loc[1, FileHeadings.ClientAccount.value]

            filename = os.path.basename(file_path)
            file_hash = self._get_file_hash(file_path)

            batch = self.stage_repo.get_stage_batch(client_account, file_hash)
            if (batch is None):
                batch = self.stage_repo.add_stage_batch(client_account, filename, file_hash)

            if (batch.batch_status == BatchStatus.Complete.value):
                raise ValueError(f'Cannot process [{filename}] file for [{batch.client_account}] account. It was already processed [{batch.end_date}]')

            success_count = 0
            failure_count = 0

            for index, row in df.iterrows():
            
                item = FileItem().create(
                    effective_date = row[FileHeadings.EffectiveDate.value],
                    client_account = row[FileHeadings.ClientAccount.value],
                    external_reference= row[FileHeadings.ExternalReference.value],
                    company_name=row[FileHeadings.CompanyName.value],
                    amount=row[FileHeadings.Amount.value], 
                    status=row[FileHeadings.Status.value])

                success = self.process_item(item, batch.id)

                if (success):
                    success_count += 1
                else:
                    failure_count += 1

            batch = self.stage_repo.complete_batch(batch.id, success_count, failure_count, 0.2)
            return batch       
           
        except Exception as ex:
            # print(f"Oops! {ex.__class__} occurred. Details: {ex}")  
            raise # re-throw after writing error to screen




        



         

        
          
