from datetime import datetime
import os
import glob
from src.data_access.database.common.database import get_db_Session, engine
from src.application.services.file_processing_service import FileProcessingService
from src.application.models.batch_status import BatchStatus
from src.data_access.database.models import database_models

context = get_db_Session()
file_service = FileProcessingService(context)

def main():
    original_file_name = None
    working_file_path = None

    try:
        directory = os.getcwd()
        root_folder = f'{directory}\\etl\\'
        database_models.Base.metadata.create_all(engine) # Create/Sync database
        
        for file in glob.glob(f"{root_folder}*.xlsx"):
            original_file_name = os.path.basename(file)
            new_filename = f'{datetime.now().strftime("%d%m%Y_%H%M%S")}_{original_file_name}'
            working_file_path = f'{root_folder}processing\\{new_filename}'

            # Move to working folder
            os.rename(file, working_file_path)
            batch_summary = file_service.process_file(working_file_path)

            if (batch_summary.batch_status == BatchStatus.Ready.value):
                # Archive file on success
                os.rename(working_file_path, f'{root_folder}archive\\{new_filename}')                      

        context.commit()
    except Exception as ex:
        print(f"Oops! {ex.__class__} occurred. Details: {ex}")
        if (os.path.isfile(working_file_path)):
            # Move file back
            os.rename(working_file_path, f'{root_folder}{original_file_name}')  

    finally:
        context.close()

main()