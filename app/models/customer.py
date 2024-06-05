from app import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Customer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)

