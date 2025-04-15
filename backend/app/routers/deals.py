from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.config import get_db
from ..models.account import Account
from ..models.deal import Deal, Review
from ..schemas.deal import Deal as DealSchema
from ..schemas.deal import DealCreate, DealStatus, DealUpdate
from ..schemas.deal import Review as ReviewSchema
from ..schemas.deal import ReviewCreate, ReviewUpdate

router = APIRouter()


@router.post("/deals/", response_model=DealSchema)
async def create_deal(deal: DealCreate, db: AsyncSession = Depends(get_db)):
    """Создание новой сделки"""
    # Проверяем доступность аккаунта
    query = select(Account).where(Account.id == deal.account_id)
    result = await db.execute(query)
    account = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if not account.is_available:
        raise HTTPException(status_code=400, detail="Account is not available")

    # Создаем сделку
    db_deal = Deal(
        seller_id=deal.seller_id,
        buyer_id=deal.buyer_id,
        account_id=deal.account_id,
        status=deal.status,
    )

    # Помечаем аккаунт как недоступный
    account.is_available = False

    db.add(db_deal)
    await db.commit()
    await db.refresh(db_deal)
    return db_deal


@router.get("/deals/", response_model=List[DealSchema])
async def read_deals(
    skip: int = 0, limit: int = 100, status: DealStatus = None, db: AsyncSession = Depends(get_db)
):
    """Получение списка сделок с фильтрацией по статусу"""
    query = select(Deal)
    if status:
        query = query.where(Deal.status == status)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    deals = result.scalars().all()
    return deals


@router.get("/deals/{deal_id}", response_model=DealSchema)
async def read_deal(deal_id: int, db: AsyncSession = Depends(get_db)):
    """Получение информации о сделке по ID"""
    query = select(Deal).where(Deal.id == deal_id)
    result = await db.execute(query)
    deal = result.scalar_one_or_none()

    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/deals/{deal_id}", response_model=DealSchema)
async def update_deal(deal_id: int, deal: DealUpdate, db: AsyncSession = Depends(get_db)):
    """Обновление статуса сделки"""
    query = select(Deal).where(Deal.id == deal_id)
    result = await db.execute(query)
    db_deal = result.scalar_one_or_none()

    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Обновляем статус
    if deal.status:
        db_deal.status = deal.status
        # Если сделка отменена, возвращаем аккаунт в доступные
        if deal.status == DealStatus.CANCELLED:
            account_query = select(Account).where(Account.id == db_deal.account_id)
            account_result = await db.execute(account_query)
            account = account_result.scalar_one_or_none()
            if account:
                account.is_available = True

    await db.commit()
    await db.refresh(db_deal)
    return db_deal


@router.post("/deals/{deal_id}/reviews/", response_model=ReviewSchema)
async def create_review(deal_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    """Создание отзыва для сделки"""
    # Проверяем существование сделки
    deal_query = select(Deal).where(Deal.id == deal_id)
    deal_result = await db.execute(deal_query)
    deal = deal_result.scalar_one_or_none()

    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    if deal.status != DealStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Can only review completed deals")

    # Проверяем, нет ли уже отзыва
    review_query = select(Review).where(Review.deal_id == deal_id)
    review_result = await db.execute(review_query)
    existing_review = review_result.scalar_one_or_none()

    if existing_review:
        raise HTTPException(status_code=400, detail="Review already exists")

    # Создаем отзыв
    db_review = Review(deal_id=deal_id, rating=review.rating, comment=review.comment)

    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


@router.get("/deals/{deal_id}/review/", response_model=ReviewSchema)
async def read_deal_review(deal_id: int, db: AsyncSession = Depends(get_db)):
    """Получение отзыва для сделки"""
    query = select(Review).where(Review.deal_id == deal_id)
    result = await db.execute(query)
    review = result.scalar_one_or_none()

    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/deals/{deal_id}/review/", response_model=ReviewSchema)
async def update_review(deal_id: int, review: ReviewUpdate, db: AsyncSession = Depends(get_db)):
    """Обновление отзыва"""
    query = select(Review).where(Review.deal_id == deal_id)
    result = await db.execute(query)
    db_review = result.scalar_one_or_none()

    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # Обновляем только предоставленные поля
    for field, value in review.dict(exclude_unset=True).items():
        setattr(db_review, field, value)

    await db.commit()
    await db.refresh(db_review)
    return db_review
