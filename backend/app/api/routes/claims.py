from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.core.db import execute_query, execute_one
from app.schemas.models import Claim, ClaimCreate, ClaimStatus, Damage

router = APIRouter()

class ClaimStatusUpdate(BaseModel):
    status: ClaimStatus


@router.get("/", response_model=List[Claim])
async def get_claims():
    """Obtener todas las reclamaciones"""
    claims_query = "SELECT id, title, description, status FROM claims ORDER BY id"
    claims_data = await execute_query(claims_query)
    
    claims = []
    for claim_row in claims_data:
        claim_id, title, description, status = claim_row
        
        # Obtener daños para cada claim
        damages_query = "SELECT id, part, severity, image_url, price, score FROM damages WHERE claim_id = %s"
        damages_data = await execute_query(damages_query, (claim_id,))
        
        damages = [
            Damage(
                id=d[0], part=d[1], severity=d[2], 
                image_url=d[3], price=d[4], score=d[5], claim_id=claim_id
            ) for d in damages_data
        ]
        
        claims.append(Claim(
            id=claim_id, title=title, description=description, 
            status=status, damages=damages
        ))
    
    return claims


@router.get("/{claim_id}", response_model=Claim)
async def get_claim(claim_id: int):
    """Obtener una reclamación específica"""
    claim_query = "SELECT id, title, description, status FROM claims WHERE id = %s"
    claim_data = await execute_one(claim_query, (claim_id,))
    
    if not claim_data:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    # Obtener daños
    damages_query = "SELECT id, part, severity, image_url, price, score, claim_id FROM damages WHERE claim_id = %s"
    damages_data = await execute_query(damages_query, (claim_id,))
    
    damages = [
        Damage(
            id=d[0], part=d[1], severity=d[2], 
            image_url=d[3], price=d[4], score=d[5], claim_id=d[6]
        ) for d in damages_data
    ]
    
    return Claim(
        id=claim_data[0], title=claim_data[1], 
        description=claim_data[2], status=claim_data[3], damages=damages
    )


@router.post("/", response_model=Claim, status_code=201)
async def create_claim(claim: ClaimCreate):
    """Crear una nueva reclamación"""
    query = """
    INSERT INTO claims (title, description, status) 
    VALUES (%s, %s, %s) RETURNING id
    """
    result = await execute_one(query, (claim.title, claim.description, claim.status))
    
    if not result:
        raise HTTPException(status_code=500, detail="Error creating claim")
    
    return Claim(id=result[0], **claim.model_dump(), damages=[])


@router.patch("/{claim_id}/status", response_model=Claim)
async def update_claim_status(claim_id: int, payload: ClaimStatusUpdate):
    # 1) Traer claim actual
    row = await execute_one("SELECT id, title, description, status FROM claims WHERE id = %s", (claim_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Claim not found")

    _id, title, description, current_status = row
    new_status = payload.status.value  # Enum -> str

    # 2) Regla: CANCELED solo desde PENDING
    if new_status == "CANCELED" and current_status != "PENDING":
        raise HTTPException(status_code=409, detail="Only PENDING claims can be CANCELED")

    # 3) Regla: si hay algún daño HIGH, description > 100 para FINALIZED
    if new_status == "FINALIZED":
        high_exists = await execute_one(
            "SELECT 1 FROM damages WHERE claim_id = %s AND severity = %s LIMIT 1",
            (claim_id, "HIGH")
        )
        if high_exists and (not description or len(description) <= 100):
            raise HTTPException(
                status_code=409,
                detail="Claims with HIGH severity damages require description > 100 chars to be FINALIZED"
            )

    # 4) Persistir estado
    updated = await execute_one(
        "UPDATE claims SET status = %s WHERE id = %s RETURNING id",
        (new_status, claim_id)
    )
    if not updated:
        raise HTTPException(status_code=500, detail="Error updating claim status")

    # 5) Devolver claim completo (reutiliza la lógica del endpoint get_claim)
    return await get_claim(claim_id)
