from typing import Any
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from datetime import datetime
from typing import Optional

class Rental(db.Model):
   
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(foreign_key=False)
    due_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=False)
    videos_checked_out_count: Mapped[int] = mapped_column(nullable=False)
    available_inventory: Mapped[int] = mapped_column(nullable=False)


#  This is a method that returns a dictionary of the object
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'video_id': self.video_id,
            'due_date': self.due_date,
            'videos_checked_out_count': self.videos_checked_out_count,
            'available_inventory': self.available_inventory}
    
# This is a class method that takes a dictionary and returns a new instance of the class
    @classmethod
    def to_object(cls, data_dict):
        return cls(
            customer_id=data_dict["customer_id"],
            video_id=data_dict["video_id"],
            due_date=data_dict["due_date"],
            videos_checked_out_count=data_dict["videos_checked_out_count"],
            available_inventory=data_dict["available_inventory"]
        )