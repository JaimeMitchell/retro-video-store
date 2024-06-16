from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
from typing import Optional

class Rental(db.Model):
    __tablename__ = 'rental'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customer.id'), nullable=False)
    video_id: Mapped[int] = mapped_column(ForeignKey('video.id'), nullable=False)
    video_title: Mapped[str] = mapped_column(nullable=False)
    due_date: Mapped[str] = mapped_column(nullable=False)
    checked_in: Mapped[bool] = mapped_column(default=False, nullable=False)

    customer: Mapped[Optional['Customer']] = relationship('Customer', back_populates='rentals')
    video: Mapped[Optional['Video']] = relationship('Video', back_populates='rentals')

    def to_dict(self):
        return {
            "id": self.id,
            'customer_id': self.customer_id,
            'video_id': self.video_id,
            'video_title': self.video_title,
            'due_date': self.due_date,
            'checked_in': self.checked_in
        }
    
    @classmethod
    def to_object(cls, data_dict):
        return cls(
            customer_id=data_dict["customer_id"],
            video_id=data_dict["video_id"],
            video_title=data_dict["video_title"],
            due_date=data_dict["due_date"],
            checked_in=data_dict["checked_in"]
        )
