from unicodedata import decimal
from src.common.models.term import Term

class FileItem():
    effective_date = None
    client_account = None
    external_refrence = None
    company_name = None
    amount = None
    term = None

    def create(self,
            effective_date: str, 
            client_account: str,
            external_reference: str,
            company_name: str,
            amount: str,
            term: str):

        try:

            if (amount is not None):
                self.amount = float(amount)

            if (term is not None):
                self.term = Term(term)
            
            self.effective_date = effective_date
            self.client_account = client_account
            self.external_refrence = external_reference
            self.company_name = company_name

            return self           

        except Exception as ex:
            print(f"Failed to read {client_account}/{external_reference}. from file: {ex}")  
            raise  # re-throw after writing error to screen
        

    def to_string(self):
        return f'Process Date = [{self.effective_date}] Client Account = [{self.client_account}] External Refrence = [{self.external_refrence}] Company Name = [{self.company_name}] Amount = [{self.amount}] Term = [{self.term.value}]'


   

