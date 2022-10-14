from datetime import datetime
from sqlite3 import dbapi2
from src.data_access.database.models.database_models import MasterRecordEntity, ClientAccountEntity
from src.application.models.client_account import ClientAccount
from src.application.models.master_record import MasterRecord
from src.application.models.term import Term
from src.application.models.stage_record import StageRecord
from src.data_access.database.common.repository_base import RepositoryBase
from src.application.models.process_action import ProcessAction
from sqlalchemy.sql import select
from sqlalchemy import or_, and_

class MasterRepository(RepositoryBase):

    def __init__(self, context) -> None:
        super().__init__(context, MasterRecordEntity, MasterRecord)

    def _check_for_changes(self, existing_record: MasterRecordEntity, pending_record: MasterRecordEntity):
        if (existing_record.amount != pending_record.amount):
            return True
        elif (existing_record.status != pending_record.status):
            return True
        else:
            return False

    def get_client_account(self, account_number) -> ClientAccount:
        client = self.context.query(ClientAccountEntity).filter(
            ClientAccountEntity.account_number == account_number).first() 
        
        return self.map(client, ClientAccount)

    def add_client_account(self, account_number) -> ClientAccount:
        client = ClientAccountEntity().create(account_number)
        self.context.add(client)
        self.sync(client)

        return self.map(client, ClientAccount)

    def get_next_master_record(self, id):
        # get top 1 order by from_date desc where id <> current id
        pass

    def get_master_record(self, external_reference, client_account_id, effective_date) -> MasterRecord:
            master_record = self.context.query(MasterRecordEntity).filter(
                and_(
                    MasterRecordEntity.external_reference == external_reference,
                    MasterRecordEntity.client_account_id == client_account_id,
                    MasterRecordEntity.is_deleted == False,
                    effective_date > MasterRecordEntity.from_date,
                    or_(
                        MasterRecordEntity.to_date is None,
                        effective_date < MasterRecordEntity.to_date)
                    )                
            ).first()

            return self.map(master_record)        

    def add_master_record(self, stage_record: StageRecord, client_account_id) -> StageRecord:

        existing_record = self.get_master_record(stage_record.external_reference, client_account_id, stage_record.effective_date)
        process_action = ProcessAction.Unknown

        new_master_record = MasterRecordEntity().create(
                stage_record.external_reference,
                stage_record.company_name,
                stage_record.amount,
                stage_record.term.value,                
                client_account_id,
                stage_record.effective_date,
                stage_record.batch_id
            )

        if (existing_record is not None and existing_record.from_date == new_master_record.from_date):
            raise ValueError(f'Critical Error. Duplicate insert request attempted for external reference [{stage_record.external_reference}] and account id [{client_account_id}]. Please investigate and remove duplicate before trying to proceed.')

        if (existing_record is not None and self._check_for_changes(existing_record, new_master_record) == False):
            scd_action = ProcessAction.Unchanged
            existing_record.last_updated = datetime.now()

        if (existing_record is None):
            scd_action = ProcessAction.Add
            new_master_record.to_date = None
            self.context.add(new_master_record)           

        elif (existing_record.to_date is None):
            scd_action = ProcessAction.Append
            #TODO: Check if placeholder insert is required (More than X days have passed)
            new_master_record.from_date = stage_record.effective_date
            new_master_record.to_date = None
            existing_record.to_date = new_master_record.from_date

        else:
            scd_action = ProcessAction.Merge
            # Update previous.to_date = new_master_record.from_date
            # Update new_master_record.to_date = existing.from_date
            # self.context.add(new_master_record)  
            # Sync previous

        if (existing_record is not None):
            self.sync(existing_record)

        self.sync(new_master_record)
        return scd_action