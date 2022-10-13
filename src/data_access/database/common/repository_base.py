from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class RepositoryBase(ABC):
    context = None
    db_entity_type = None
    business_entity_type = None

    def map(self, db_object, business_class = None):
        if (db_object is None):
            return None

        if business_class is None:
            business_class = self.business_entity_type

        mapped = business_class.from_orm(db_object)
        return mapped

    def map_all(self, db_objects, business_class = None):
        if (db_objects is None):
            return None

        if business_class is None:
            business_class = self.business_entity_type
        
        items = []
        for item in db_objects:
            mapped = business_class.from_orm(item)
            items.append(mapped)

    def __init__(self, context: Session, db_entity_type, business_entity_type) -> None:
        self.context = context
        self.db_entity_type = db_entity_type
        self.business_entity_type = business_entity_type

    def get(self, id):
        account = self.context.get(self.db_entity_type, id)
        return self.map(account)

    def add(self, entity):
        if not isinstance(entity, self.db_entity_type):
            raise ValueError(f'Unable to add [{entity}] not a valid [{self.db_entity_type}] entity.')
          
        self.context.add(entity)
        self.sync(entity)

        return self.map(entity)

    def delete(self, id):
        self.context.query(self.db_entity_type).filter(self.db_entity_type.id == id).delete()
        self.sync()

    def sync(self, object = None):
        self.context.flush()

        if (object is not None):
            self.context.refresh(object)
