from sqlalchemy import Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..schemas.deal import DealStatus
from .base import BaseModel


class Deal(BaseModel):
    """Модель сделки"""

    __tablename__ = "deals"

    seller_id = Column(Integer, ForeignKey("users.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    status = Column(SQLAlchemyEnum(DealStatus), default=DealStatus.PENDING)

    # Связи с другими таблицами
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sales")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="purchases")
    account = relationship("Account", back_populates="deals")
    review = relationship("Review", back_populates="deal", uselist=False)


class Review(BaseModel):
    """Модель отзыва"""

    __tablename__ = "reviews"

    deal_id = Column(Integer, ForeignKey("deals.id"), unique=True)
    rating = Column(Integer)
    comment = Column(String, nullable=True)

    # Связь с таблицей сделок
    deal = relationship("Deal", back_populates="review")
