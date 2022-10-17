from datetime import datetime
from doctest import master
import os
import glob

from src.data_access.database.common.database import get_db_Session, engine
from src.application.services.file_processing_service import FileProcessingService
from src.application.services.scd_service import SCDService
from src.common.models.batch_status import BatchStatus
from src.data_access.database.models import database_models

def clean_orphaned_batches(root_folder):
    processing_folder = f'{root_folder}processing\\'
    context = get_db_Session()

    for file in glob.glob(f"{processing_folder}*.xlsx"):
        file_name = os.path.basename(file)
        original_file_name = file_name[16:]
        
        os.rename(file, f'{root_folder}{original_file_name}')  
        context.commit()


def etl_to_stage():

    try:
        directory = os.getcwd()
        original_file_name = None
        working_file_path = None
        root_folder = f'{directory}\\etl\\'    

        clean_orphaned_batches(root_folder)
        
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
    try:
      context = get_db_Session()
      service = SCDService(context)

      service.process_staged_records()

    except Exception as ex:
        print(f"Oops! {ex.__class__} occurred. Details: {ex}")


def main():
    database_models.Base.metadata.create_all(engine) # Create/Sync database    
    # TODO: Move to seperate schedule
    etl_to_stage()

    # TODO: Move to seperate schedule
    process_ready_batched()

main()