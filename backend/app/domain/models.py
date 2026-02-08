from enum import Enum
from decimal import Decimal, InvalidOperation
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import Enum as SQLEnum

from app.core.db import Base


class ClaimStatus(str, Enum):
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    FINALIZED = "FINALIZED"
    CANCELED = "CANCELED"


class DamageSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(ClaimStatus), default=ClaimStatus.PENDING, nullable=False)
    
    damages = relationship("Damage", back_populates="claim", cascade="all, delete-orphan")

    @property
    def total_amount(self) -> Decimal:
        total = Decimal("0.00")
        for d in self.damages:
            # d.price debería ser Decimal al venir de Numeric
            total += (d.price or Decimal("0.00"))
        return total


class Damage(Base):
    __tablename__ = "damages"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    severity = Column(SQLEnum(DamageSeverity), nullable=False)
    image_url = Column(String(500), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    score = Column(Integer, nullable=False)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    
    claim = relationship("Claim", back_populates="damages")

    @validates("price")
    def validate_price(self, key, value):
        """
        Rules:
        - Mandatory
        - Decimal
        - >= 0
        - with 2 decimals (consistent rounding)
        """
        if value is None:
            raise ValueError("price is required")

        # Acepta Decimal, int, str, float (float lo convertimos a str para minimizar errores)
        try:
            if isinstance(value, Decimal):
                dec = value
            elif isinstance(value, float):
                dec = Decimal(str(value))
            else:
                dec = Decimal(value)
        except (InvalidOperation, TypeError):
            raise ValueError("price must be a valid decimal number")

        if dec < 0:
            raise ValueError("price must be >= 0")

        # Normaliza a 2 decimales (coherente con Numeric(10,2))
        dec = dec.quantize(Decimal("0.01"))
        return dec

    @validates("score")
    def validate_score(self, value):
        """
        Rules:
        - Mandatory
        - Integer
        - 1 - 10
        """
        if value is None:
            raise ValueError("score is required")

        # Evita bool (True/False)
        if isinstance(value, bool):
            raise ValueError("score must be an integer between 1 and 10")

        try:
            ivalue = int(value)
        except (TypeError, ValueError):
            raise ValueError("score must be an integer between 1 and 10")

        if not (1 <= ivalue <= 10):
            raise ValueError("score must be between 1 and 10")

        return ivalue