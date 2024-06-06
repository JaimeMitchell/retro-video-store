from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Customer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)

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