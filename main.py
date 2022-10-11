import os

from src.application.services.file_processing_service import FileProcessingService


def main():
    directory = os.getcwd()
    file_path = f'{directory}/etl/sample_files/ExampleFile.xlsx'

    service = FileProcessingService()
    service.process_file(file_path)


main()