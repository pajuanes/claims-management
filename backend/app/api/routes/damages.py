from fastapi import APIRouter, HTTPException, Response
from typing import List
from app.core.db import execute_query, execute_one
from app.schemas.models import Damage, DamageCreate

router = APIRouter()


@router.get("/", response_model=List[Damage])
async def get_damages():
    """Obtener todos los daños"""
    query = "SELECT id, part, severity, image_url, price, score, claim_id FROM damages ORDER BY id"
    damages_data = execute_query(query)
    
    return [
        Damage(
            id=d[0], part=d[1], severity=d[2], 
            image_url=d[3], price=d[4], score=d[5], claim_id=d[6]
        ) for d in damages_data
    ]


@router.post("/", response_model=Damage)
async def create_damage(damage: DamageCreate, claim_id: int):
    """Crear un nuevo daño"""

    # 1) Verificar que el claim existe y obtener status del claim
    claim_row = execute_one("SELECT id, status FROM claims WHERE id = %s", (claim_id,))
    if not claim_row:
        raise HTTPException(status_code=404, detail="Claim not found")

    # Solo se pueden agregar daños a claims en estado PENDING
    _, status = claim_row
    if status != "PENDING":
        raise HTTPException(status_code=409, detail="Damages can only be managed when claim is PENDING")
    
    # 2) Crear
    query = """
    INSERT INTO damages (part, severity, image_url, price, score, claim_id) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    """
    result = execute_one(query, (
        damage.part, damage.severity.value if hasattr(damage.severity, "value") else damage.severity,
        str(damage.image_url), damage.price, damage.score, claim_id
    ))
    
    if not result:
        raise HTTPException(status_code=500, detail="Error creating damage")
    
    return Damage(id=result[0], claim_id=claim_id, **damage.model_dump())


@router.put("/{damage_id}", response_model=Damage)
async def update_damage(damage_id: int, damage: DamageCreate):
    """Editar un daño existente (solo si el claim está en PENDING)"""

    # 1) Verificar que el daño existe y obtener status del claim
    row = execute_one("""
        SELECT d.claim_id, c.status
        FROM damages d
        JOIN claims c ON c.id = d.claim_id
        WHERE d.id = %s
    """, (damage_id,))

    if not row:
        raise HTTPException(status_code=404, detail="Damage not found")
    
    # Solo se pueden actualizar daños a claims en estado PENDING
    claim_id, status = row
    if status != "PENDING":
        raise HTTPException(status_code=409, detail="Damages can only be managed when claim is PENDING")

    # 2) Actualizar
    result = execute_one("""
        UPDATE damages
        SET part = %s, severity = %s, image_url = %s, price = %s, score = %s
        WHERE id = %s
        RETURNING id
    """, (
        damage.part,
        damage.severity.value if hasattr(damage.severity, "value") else damage.severity,
        str(damage.image_url),
        damage.price,
        damage.score,
        damage_id
    ))

    if not result:
        raise HTTPException(status_code=500, detail="Error updating damage")

    return Damage(id=damage_id, claim_id=claim_id, **damage.model_dump())


@router.delete("/{damage_id}", status_code=204)
async def delete_damage(damage_id: int):
    """Eliminar un daño (solo si el claim está en PENDING)"""

    # 1) Verificar que el daño existe y obtener status del claim
    row = execute_one("""
        SELECT d.claim_id, c.status
        FROM damages d
        JOIN claims c ON c.id = d.claim_id
        WHERE d.id = %s
    """, (damage_id,))

    if not row:
        raise HTTPException(status_code=404, detail="Damage not found")

    _, status = row
    if status != "PENDING":
        raise HTTPException(status_code=409, detail="Damages can only be managed when claim is PENDING")

    # 2) Borrar
    deleted = execute_one("DELETE FROM damages WHERE id = %s RETURNING id", (damage_id,))
    if not deleted:
        raise HTTPException(status_code=500, detail="Error deleting damage")

    return Response(status_code=204)
