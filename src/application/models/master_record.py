from src.application.models.record_status import RecordStatus

class MasterRecord():
    id = None
    external_reference = None
    company_name = None
    amount = None
    status = None
    from_date = None
    to_date = None
    last_updated = None
    is_deleted = None
    has_changes = None
    batch_id = None
    client_account_id = None
    
    def create(self, 
            external_reference, 
            company_name, 
            amount, 
            status,
            from_date, 
            to_date, 
            last_updated,
            is_deleted,
            has_changes,
            batch_id,
            client_account_id,
            id = None):

        self.id = id
        self.external_reference = external_reference
        self.company_name = company_name
        self.amount = amount
        self.status = RecordStatus[status]
        self.from_date = from_date
        self.to_date = to_date
        self.last_updated = last_updated
        self.is_deleted = is_deleted
        self.has_changes = has_changes
        self.batch_id = batch_id
        self.client_account_id = client_account_id
        
        return self
    