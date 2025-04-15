from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """Модель пользователя"""

    __tablename__ = "users"

    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True)
    rating = Column(Float, default=0.0)

    # Связи с другими таблицами
    sales = relationship("Deal", foreign_keys="[Deal.seller_id]", back_populates="seller")
    purchases = relationship("Deal", foreign_keys="[Deal.buyer_id]", back_populates="buyer")
