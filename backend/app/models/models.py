from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """Модель пользователя"""

    __tablename__ = "users"

    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(50), unique=True)
    rating = Column(Float, default=0.0)

    # Связи
    accounts = relationship("Account", back_populates="user")
    sales = relationship("Deal", back_populates="seller", foreign_keys="Deal.seller_id")
    purchases = relationship("Deal", back_populates="buyer", foreign_keys="Deal.buyer_id")


class Account(BaseModel):
    """Модель игрового аккаунта"""

    __tablename__ = "accounts"

    user_id = Column(Integer, ForeignKey("users.id"))
    game = Column(String(100))
    description = Column(Text)
    price = Column(Float)

    # Связи
    user = relationship("User", back_populates="accounts")
    deal = relationship("Deal", back_populates="account", uselist=False)


class Deal(BaseModel):
    """Модель сделки"""

    __tablename__ = "deals"

    seller_id = Column(Integer, ForeignKey("users.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    status = Column(String(20), default="pending")  # pending, completed, cancelled

    # Связи
    seller = relationship("User", back_populates="sales", foreign_keys=[seller_id])
    buyer = relationship("User", back_populates="purchases", foreign_keys=[buyer_id])
    account = relationship("Account", back_populates="deal")
    review = relationship("Review", back_populates="deal", uselist=False)


class Review(BaseModel):
    """Модель отзыва"""

    __tablename__ = "reviews"

    deal_id = Column(Integer, ForeignKey("deals.id"))
    rating = Column(Integer)  # 1-5
    comment = Column(Text)

    # Связи
    deal = relationship("Deal", back_populates="review")
