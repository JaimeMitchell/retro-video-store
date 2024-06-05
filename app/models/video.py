from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Video(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[datetime] = mapped_column(nullable=False)
    total_inventory: Mapped[int] = mapped_column(nullable=False)


