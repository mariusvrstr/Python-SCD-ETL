import pandas as pd
from src.contracts.template.FileHeadings import FileHeadings
from src.contracts.template.FileItem import FileItem

class FileProcessingService():

    def process_item(self, item: FileItem):
        print(item.to_string())

    def process_file(self, path):
        data = pd.read_excel(path)
        df = pd.DataFrame(data)   

        for index, row in df.iterrows():
            
            item = FileItem().create(
                effective_date = row[FileHeadings.EffectiveDate.value],
                client_account = row[FileHeadings.ClientAccount.value],
                external_reference= row[FileHeadings.ExternalReference.value],
                company_name=row[FileHeadings.CompanyName.value],
                amount=row[FileHeadings.Amount.value],
                status=row[FileHeadings.Status.value])

            self.process_item(item)
          
