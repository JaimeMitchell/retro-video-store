from app import db
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from typing import Optional

class Customer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    registered_at: Mapped[datetime.datetime]
    postal_code: Mapped[str]
    phone: Mapped[str]
    
#  This is a method that returns a dictionary of the object
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'registered_at': self.registered_at,
            'postal_code': self.postal_code,
            'phone': self.phone}

# This is a class method that takes a dictionary and returns a new instance of the class
    @classmethod
    def to_object(cls, data_dict):
        return cls(
            id=data_dict["id"],
            name=data_dict["name"],
            registered_at=data_dict["registered_at"],
            postal_code=data_dict["postal_code"],
            phone=data_dict["phone"]
        )