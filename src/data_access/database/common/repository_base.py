from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class RepositoryBase(ABC):
    context = None
    db_entity_type = None
    business_entity_type = None

    def map(self, type, db_object):
        if (db_object is None):
            return None

        mapped = type.from_orm(db_object)
        return mapped

    def map_all(self, type, db_objects):
        if (db_objects is None):
            return None
        
        items = []
        for item in db_objects:
            mapped = type.from_orm(item)
            items.append(mapped)

    def __init__(self, context: Session, db_entity_type, business_entity_type) -> None:
        self.context = context
        self.db_entity_type = db_entity_type
        self.business_entity_type = business_entity_type

    def get(self, id):
        account = self.context.get(self.db_entity_type, id)
        mapped = self.business_entity_type.from_orm(account)
        return mapped

    def add(self, entity):
        if not isinstance(entity, self.db_entity_type):
            raise ValueError(f'Unable to add [{entity}] not a valid [{self.db_entity_type}] entity.')
          
        self.context.add(entity)
        self.sync(entity)

        mapped = self.business_entity_type.from_orm(entity)
        return mapped

    def delete(self, id):
        self.context.query(self.db_entity_type).filter(self.db_entity_type.id == id).delete()
        self.sync()

    def sync(self, object = None):
        self.context.flush()

        if (object is not None):
            self.context.refresh(object)
