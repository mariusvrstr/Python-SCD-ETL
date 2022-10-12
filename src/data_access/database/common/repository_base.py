from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class RepositoryBase(ABC):
    context = None
    db_entity_type = None
    business_entity_type = None

    @abstractmethod
    def map_to_business(self, database_object) -> business_entity_type:
        pass

    @abstractmethod
    def map_to_database(self, business_object) -> db_entity_type:
        pass

    def __init__(self, context: Session, db_entity_type, business_entity_type) -> None:
        self.context = context
        self.db_entity_type = db_entity_type
        self.business_entity_type = business_entity_type

    def get(self, id):
        account = self.context.get(self.db_entity_type, id)
        return self.map_to_business(account)

    def add(self, entity):
        db_entity = None

        if (isinstance(entity, self.business_entity_type)):
            db_entity = self.map_to_database(entity)            
        elif(isinstance(entity, self.db_entity_type)):
            db_entity = entity

        if (db_entity == None):
            raise ValueError(f'Unable to add [{entity}] not a valid entity.')

        self.context.add(db_entity)
        self.sync(db_entity)

        return self.map_to_business(db_entity)

    def delete(self, id):
        self.context.query(self.db_entity_type).filter(self.db_entity_type.id == id).delete()
        self.sync()

    def sync(self, object = None):
        self.context.flush()

        if (object is not None):
            self.context.refresh(object)
