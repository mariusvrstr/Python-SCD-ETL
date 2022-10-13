from datetime import datetime
import os
import glob
from src.application.models.process_status import ProcessStatus
from src.application.models.stage_record import StageRecord
from src.data_access.database.common.database import get_db_Session, engine
from src.application.services.file_processing_service import FileProcessingService
from src.application.models.batch_status import BatchStatus
from src.data_access.database.master_repository import MasterRepository
from src.data_access.database.models import database_models
from src.data_access.database.stage_repository import StageRepository

def etl_to_stage():

    try:
        directory = os.getcwd()
        original_file_name = None
        working_file_path = None
        root_folder = f'{directory}\\etl\\'        
        
        for file in glob.glob(f"{root_folder}*.xlsx"):
            context = get_db_Session()
            file_service = FileProcessingService(context)
            
            try: 
                original_file_name = os.path.basename(file)
                new_filename = f'{datetime.now().strftime("%d%m%Y_%H%M%S")}_{original_file_name}'
                working_file_path = f'{root_folder}processing\\{new_filename}'

                 # Move to working folder
                os.rename(file, working_file_path)
                batch_summary = file_service.process_file(working_file_path)

                # On Failure
                if (batch_summary.batch_status != BatchStatus.Ready):
                    raise ValueError(f'File [{file}] not successfully processed, expecting to be in Ready status but is [{batch_summary.batch_status.value}]')
            
                # Archive on Success
                os.rename(working_file_path, f'{root_folder}archive\\{new_filename}')
                context.commit()

            except Exception as ex:
                # If one file fails it should not impact others from processing
                print(f"Oops! {ex.__class__} occurred. Details: {ex}")
                context.rollback()

                if (os.path.isfile(working_file_path)):
                    os.rename(working_file_path, f'{root_folder}{original_file_name}')  
            
            finally:
                context.close()          

    except Exception as ex:
        print(f"Oops! {ex.__class__} occurred. Details: {ex}")


def process_ready_batched():
    context = get_db_Session()   
    
    try:
        stage_repo = StageRepository(context)
        batches = stage_repo.get_ready_batches()

        for batch in batches:
            
            try:
                stage_records = stage_repo.get_batched_stage_records(batch.id, ProcessStatus.Unprocessed, 5)

                while len(stage_records) > 0:
                    context = get_db_Session()
                    stage_repo = StageRepository(context)
                    master_repo = MasterRepository(context)

                    while len(stage_records) > 0:
                        record = stage_records.pop()

                        try:
                            print(f'SCD THE STAGE RECORD ID [{record.id}]/ BATC [{batch.id}]')

                            stage_repo.complete_stage_record_process(record.id, ProcessStatus.Processed)

                        except Exception as ex:
                            # If one record fails it should not impact others from processing
                            print(f"Oops! {ex.__class__} occurred. Details: {ex}")
                            stage_repo.complete_stage_record_process(record.id, ProcessStatus.Failed)

                    context.commit()
                    stage_records = stage_repo.get_batched_stage_records(batch.id, ProcessStatus.Unprocessed, 5)   

                stage_repo.complete_batch_process(batch.id)
                context.commit()

            except Exception as ex:
                # If one batch fails it should not impact others from processing
                print(f"Oops! {ex.__class__} occurred. Details: {ex}")
                context.rollback()
         
            finally:
                context.close()
     
    except Exception as ex:
        print(f"Oops! {ex.__class__} occurred. Details: {ex}")


def main():
    database_models.Base.metadata.create_all(engine) # Create/Sync database
    
    # TODO: Move to seperate schedule
    etl_to_stage()

    # TODO: Move to seperate schedule
    process_ready_batched()

main()