from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database.config import get_db
from ..models.account import Account
from ..schemas.account import Account as AccountSchema
from ..schemas.account import AccountCreate, AccountUpdate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/accounts", response_model=AccountSchema)
async def create_account(account: AccountCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового аккаунта"""
    db_account = Account(
        title=account.title,
        game=account.game,
        description=account.description,
        price=account.price,
        image_url=account.image_url,
        seller=account.seller,
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


@router.get("/accounts", response_model=List[AccountSchema])
async def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Получение списка аккаунтов"""
    logger.info(f"Executing read_accounts endpoint with skip={skip}, limit={limit}")
    query = select(Account).offset(skip).limit(limit)
    
    result = await db.execute(query)
    accounts = result.scalars().all()
    logger.info(f"Found {len(accounts)} accounts")
    return accounts


@router.get("/accounts/{account_id}", response_model=AccountSchema)
async def read_account(account_id: int, db: AsyncSession = Depends(get_db)):
    """Получение информации об аккаунте по ID"""
    query = select(Account).where(Account.id == account_id)
    result = await db.execute(query)
    account = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# @router.get("/accounts/user/{user_id}", response_model=List[AccountSchema]) # <-- Функция закомментирована, т.к. user_id удален из модели Account
# async def read_user_accounts(user_id: int, db: AsyncSession = Depends(get_db)):
#     """Получение списка аккаунтов пользователя"""
#     query = select(Account).where(Account.user_id == user_id)
#     result = await db.execute(query)
#     accounts = result.scalars().all()
#     return accounts


@router.put("/accounts/{account_id}", response_model=AccountSchema)
async def update_account(
    account_id: int, account: AccountUpdate, db: AsyncSession = Depends(get_db)
):
    """Обновление информации об аккаунте"""
    query = select(Account).where(Account.id == account_id)
    result = await db.execute(query)
    db_account = result.scalar_one_or_none()

    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # Обновляем только предоставленные поля
    for field, value in account.model_dump(exclude_unset=True).items():
        setattr(db_account, field, value)

    await db.commit()
    await db.refresh(db_account)
    return db_account


@router.delete("/accounts/{account_id}")
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление аккаунта"""
    query = select(Account).where(Account.id == account_id)
    result = await db.execute(query)
    account = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    await db.delete(account)
    await db.commit()
    return {"ok": True}
