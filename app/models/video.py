from app import db
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from typing import Optional, List


class Video(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] 
    release_date: Mapped[str] 
    total_inventory: Mapped[int]

    rentals: Mapped[List['Rental']] = relationship('Rental', back_populates='video')


#  This is a method that returns a dictionary of the object
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'total_inventory': self.total_inventory}

# This is a class method that takes a dictionary and returns a new instance of the class
    @classmethod
    def to_object(cls, data_dict):
        return cls(
            id=data_dict["id"],
            title=data_dict["title"],
            release_date=data_dict["release_date"],
            total_inventory=data_dict["total_inventory"],
        )
