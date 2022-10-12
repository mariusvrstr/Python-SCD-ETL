
class ClientAccount():
    id = None
    account_number = None
    last_updated = None

    def create(self, 
            account_number, 
            last_updated, 
            id = None):

        self.id = id
        self.account_number = account_number
        self.last_updated = last_updated

        return self
