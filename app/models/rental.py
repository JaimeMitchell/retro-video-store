from typing import Any
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from datetime import datetime

class Rental(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[datetime] = mapped_column(nullable=False)
    total_inventory: Mapped[int] = mapped_column(nullable=False)


