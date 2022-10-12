import os
from src.data_access.database.common.database import get_db_Session, engine
from src.application.services.file_processing_service import FileProcessingService
from src.data_access.database.models import database_models

context = get_db_Session()
file_service = FileProcessingService(context)

def main():

    try:
        directory = os.getcwd()
        file_path = f'{directory}\\etl\\sample_files\\ExampleFile.xlsx'
        database_models.Base.metadata.create_all(engine) # Create/Sync database

        file_service.process_file(file_path)

        context.commit()
    except Exception as ex:
        print(f"Oops! {ex.__class__} occurred. Details: {ex}")
    finally:
        context.close()

main()