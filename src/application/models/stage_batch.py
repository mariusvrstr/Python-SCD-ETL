

from datetime import datetime
from src.application.models.batch_status import BatchStatus

class StageBatch():
    id = None
    client_account = None
    start_date = None
    end_date = None
    file_hash = None
    filename = None
    success_count = None
    failure_count = None
    batch_status = None

    def create(self, client_account, start_date, end_date, file_hash, filename, success_count, failure_count, batch_status, id = None):
        self.id = id
        self.client_account = client_account
        self.start_date = start_date
        self.end_date = end_date
        self.filename = filename
        self.file_hash = file_hash
        self.success_count = success_count
        self.failure_count = failure_count       
        self.batch_status = batch_status

        return self
