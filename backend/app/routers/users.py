from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.config import get_db
from ..models.user import User
from ..schemas.user import User as UserSchema
from ..schemas.user import UserCreate, UserUpdate

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового пользователя"""
    # Проверяем, существует ли пользователь с таким telegram_id
    query = select(User).where(User.telegram_id == user.telegram_id)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(telegram_id=user.telegram_id, username=user.username, rating=user.rating)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[UserSchema])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Получение списка пользователей"""
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получение информации о пользователе по ID"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/telegram/{telegram_id}", response_model=UserSchema)
async def read_user_by_telegram(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Получение информации о пользователе по Telegram ID"""
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    """Обновление информации о пользователе"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем только предоставленные поля
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление пользователя"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"ok": True}
