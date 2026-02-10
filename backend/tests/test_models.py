import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.models import (
    ClaimStatus, DamageSeverity,
    DamageCreate, Damage,
    ClaimCreate, Claim
)


def test_claim_status_enum():
    """Test ClaimStatus enum values"""
    assert ClaimStatus.PENDING == "PENDING"
    assert ClaimStatus.IN_REVIEW == "IN_REVIEW"
    assert ClaimStatus.FINALIZED == "FINALIZED"
    assert ClaimStatus.CANCELED == "CANCELED"


def test_damage_severity_enum():
    """Test DamageSeverity enum values"""
    assert DamageSeverity.LOW == "LOW"
    assert DamageSeverity.MEDIUM == "MEDIUM"
    assert DamageSeverity.HIGH == "HIGH"


def test_normalize_price_from_float():
    """Test normalize_price converts float to Decimal with 2 decimals"""
    damage = DamageCreate(
        part="Bumper",
        severity=DamageSeverity.LOW,
        image_url="http://example.com/img.jpg",
        price=100.5,
        score=5
    )
    assert damage.price == Decimal("100.50")
    assert isinstance(damage.price, Decimal)


def test_normalize_price_from_int():
    """Test normalize_price converts int to Decimal with 2 decimals"""
    damage = DamageCreate(
        part="Door",
        severity=DamageSeverity.MEDIUM,
        image_url="http://example.com/img.jpg",
        price=200,
        score=7
    )
    assert damage.price == Decimal("200.00")


def test_normalize_price_from_string():
    """Test normalize_price converts string to Decimal with 2 decimals"""
    damage = DamageCreate(
        part="Hood",
        severity=DamageSeverity.HIGH,
        image_url="http://example.com/img.jpg",
        price="150.75",
        score=9
    )
    assert damage.price == Decimal("150.75")


def test_normalize_price_from_decimal():
    """Test normalize_price handles Decimal input"""
    damage = DamageCreate(
        part="Mirror",
        severity=DamageSeverity.LOW,
        image_url="http://example.com/img.jpg",
        price=Decimal("99.999"),
        score=4
    )
    assert damage.price == Decimal("100.00")


def test_damage_create_valid():
    """Test DamageCreate with valid data"""
    damage = DamageCreate(
        part="Bumper",
        severity=DamageSeverity.LOW,
        image_url="http://example.com/img.jpg",
        price=100.50,
        score=5
    )
    assert damage.part == "Bumper"
    assert damage.severity == DamageSeverity.LOW
    assert damage.price == Decimal("100.50")
    assert damage.score == 5


def test_damage_with_id():
    """Test Damage model with id and claim_id"""
    damage = Damage(
        id=1,
        claim_id=10,
        part="Door",
        severity=DamageSeverity.MEDIUM,
        image_url="http://example.com/img.jpg",
        price=200.00,
        score=7
    )
    assert damage.id == 1
    assert damage.claim_id == 10


def test_damage_invalid_score_low():
    """Test Damage validation fails for score < 1"""
    with pytest.raises(ValidationError) as exc_info:
        DamageCreate(
            part="Bumper",
            severity=DamageSeverity.LOW,
            image_url="http://example.com/img.jpg",
            price=100.00,
            score=0
        )
    assert "score" in str(exc_info.value)


def test_damage_invalid_score_high():
    """Test Damage validation fails for score > 10"""
    with pytest.raises(ValidationError) as exc_info:
        DamageCreate(
            part="Bumper",
            severity=DamageSeverity.LOW,
            image_url="http://example.com/img.jpg",
            price=100.00,
            score=11
        )
    assert "score" in str(exc_info.value)


def test_damage_invalid_price_negative():
    """Test Damage validation fails for negative price"""
    with pytest.raises(ValidationError) as exc_info:
        DamageCreate(
            part="Bumper",
            severity=DamageSeverity.LOW,
            image_url="http://example.com/img.jpg",
            price=-50.00,
            score=5
        )
    assert "price" in str(exc_info.value)


def test_claim_create_valid():
    """Test ClaimCreate with valid data"""
    claim = ClaimCreate(
        title="Test Claim",
        description="Test description",
        status=ClaimStatus.PENDING
    )
    assert claim.title == "Test Claim"
    assert claim.description == "Test description"
    assert claim.status == ClaimStatus.PENDING


def test_claim_create_default_status():
    """Test ClaimCreate uses PENDING as default status"""
    claim = ClaimCreate(
        title="Test Claim"
    )
    assert claim.status == ClaimStatus.PENDING
    assert claim.description is None


def test_claim_with_damages():
    """Test Claim model with damages list"""
    damage1 = Damage(
        id=1,
        claim_id=1,
        part="Bumper",
        severity=DamageSeverity.LOW,
        image_url="http://example.com/img1.jpg",
        price=100.00,
        score=5
    )
    damage2 = Damage(
        id=2,
        claim_id=1,
        part="Door",
        severity=DamageSeverity.MEDIUM,
        image_url="http://example.com/img2.jpg",
        price=200.00,
        score=7
    )
    
    claim = Claim(
        id=1,
        title="Test Claim",
        description="Test",
        status=ClaimStatus.PENDING,
        damages=[damage1, damage2]
    )
    
    assert len(claim.damages) == 2
    assert claim.damages[0].part == "Bumper"
    assert claim.damages[1].part == "Door"


def test_claim_total_amount_empty():
    """Test total_amount property with no damages"""
    claim = Claim(
        id=1,
        title="Test Claim",
        status=ClaimStatus.PENDING,
        damages=[]
    )
    assert claim.total_amount == Decimal("0.00")


def test_claim_total_amount_with_damages():
    """Test total_amount property calculates sum of damage prices"""
    damage1 = Damage(
        id=1,
        claim_id=1,
        part="Bumper",
        severity=DamageSeverity.LOW,
        image_url="http://example.com/img1.jpg",
        price=100.50,
        score=5
    )
    damage2 = Damage(
        id=2,
        claim_id=1,
        part="Door",
        severity=DamageSeverity.MEDIUM,
        image_url="http://example.com/img2.jpg",
        price=250.75,
        score=7
    )
    
    claim = Claim(
        id=1,
        title="Test Claim",
        status=ClaimStatus.PENDING,
        damages=[damage1, damage2]
    )
    
    assert claim.total_amount == Decimal("351.25")
