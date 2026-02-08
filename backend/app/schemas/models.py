from enum import Enum
from typing import List, Optional
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, AnyUrl, field_validator


class ClaimStatus(str, Enum):
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    FINALIZED = "FINALIZED"
    CANCELED = "CANCELED"


class DamageSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


Price = Annotated[
    Decimal,
    Field(ge=Decimal("0"), max_digits=10, decimal_places=2)
]

Score = Annotated[
    int,
    Field(ge=1, le=10)
]


class DamageBase(BaseModel):
    part: str
    severity: DamageSeverity
    image_url: AnyUrl
    price: Price
    score: Score

    @field_validator("price", mode="before")
    @classmethod
    def normalize_price(cls, v):
        """
        Acepta int/float/str y normaliza siempre a 2 decimales.
        """
        if isinstance(v, float):
            v = Decimal(str(v))
        if not isinstance(v, Decimal):
            v = Decimal(v)
        return v.quantize(Decimal("0.01"))


class DamageCreate(DamageBase):
    pass


class Damage(DamageBase):
    id: int
    claim_id: int


class ClaimBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: ClaimStatus = ClaimStatus.PENDING


class ClaimCreate(ClaimBase):
    pass


class Claim(ClaimBase):
    id: int
    damages: List[Damage] = []

    @property
    def total_amount(self) -> Decimal:
        return sum((d.price for d in self.damages), Decimal("0.00"))
