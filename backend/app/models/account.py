from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel


class Account(BaseModel):
    """Модель игрового аккаунта"""

    __tablename__ = "accounts"

    title = Column(String, index=True)
    game = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    seller = Column(JSON, default=lambda: {"id": 0, "name": "Unknown", "rating": 0})
    is_available = Column(Boolean, default=True)

    # Связи с другими таблицами
    deals = relationship("Deal", back_populates="account")
