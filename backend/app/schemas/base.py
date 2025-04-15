from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Базовая схема для всех моделей"""

    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Используем model_config для Pydantic v2
    model_config = {
        "from_attributes": True
    }
