from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.account import Account
from ..models.user import User


async def seed_users(db: AsyncSession):
    """Заполняем базу тестовыми пользователями"""
    result = await db.execute(select(User))
    if result.scalars().first():
        print("Пользователи уже существуют, сидинг пользователей не требуется.")
        return

    print("Создание тестовых пользователей...")
    test_users = [
        User(
            id=1,
            telegram_id=123456789,
            username="testuser1",
            rating=4.5
        ),
        User(
            id=2,
            telegram_id=987654321,
            username="testuser2",
            rating=5.0
        )
    ]

    db.add_all(test_users)
    await db.commit()
    print("Тестовые пользователи созданы.")

async def seed_accounts(db: AsyncSession):
    """Заполняем базу тестовыми аккаунтами"""
    result = await db.execute(select(Account))
    if result.scalars().first():
        print("Аккаунты уже существуют, сидинг аккаунтов не требуется.")
        return
    
    print("Создание тестовых аккаунтов...")
    test_accounts = [
        Account(
            title="Аккаунт Dota 2 Immortal",
            game="Dota 2",
            description="Immortal rank, 6000 MMR, все герои открыты",
            price=15000,
            image_url="https://example.com/dota2.jpg",
            seller={"id": 1, "name": "testuser1", "rating": 4.5},
            is_available=True
        ),
        Account(
            title="Аккаунт CS:GO Global Elite",
            game="CS:GO",
            description="Global Elite, инвентарь на 50к",
            price=25000,
            image_url="https://example.com/csgo.jpg",
            seller={"id": 1, "name": "testuser1", "rating": 4.5},
            is_available=True
        ),
        Account(
            title="Аккаунт World of Warcraft 70 lvl",
            game="World of Warcraft",
            description="70 level, полная экипировка",
            price=8000,
            image_url="https://example.com/wow.jpg",
            seller={"id": 2, "name": "testuser2", "rating": 5.0},
            is_available=True
        ),
        Account(
            title="Аккаунт Genshin Impact AR60",
            game="Genshin Impact",
            description="AR 60, все персонажи 90 уровня",
            price=45000,
            image_url="https://example.com/genshin.jpg",
            seller={"id": 2, "name": "testuser2", "rating": 5.0},
            is_available=True
        ),
        Account(
            title="Аккаунт PUBG Top 100",
            game="PUBG",
            description="Топ 100 игрок, редкие скины",
            price=12000,
            image_url="https://example.com/pubg.jpg",
            seller={"id": 1, "name": "testuser1", "rating": 4.5},
            is_available=True
        )
    ]

    db.add_all(test_accounts)
    await db.commit() 