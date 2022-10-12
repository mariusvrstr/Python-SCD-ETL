

class StageRecord():
    id = None
    effective_date = None
    insert_date = None
    external_reference = None
    company_name = None
    amount = None
    status = None

    def create(self, effective_date, insert_date, external_reference, amount, status, id = None):
        self.id = id
        self.effective_date = effective_date
        self.insert_date = insert_date
        self.external_reference = external_reference
        self.amount = amount
        self.status = status
        
        return self
    