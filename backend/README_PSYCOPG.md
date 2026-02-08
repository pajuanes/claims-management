# Claims Manager - Implementación con psycopg

## Cambios realizados

Se ha simplificado la implementación reemplazando SQLAlchemy por psycopg directo:

### Archivos modificados:
- `app/core/config.py` - Configuración simplificada
- `app/core/db.py` - Conexión directa con psycopg
- `pyproject.toml` - Dependencias actualizadas
- `app/schemas/models.py` - Modelos Pydantic (nuevo)
- `app/api/routes/claims.py` - Rutas con consultas SQL directas
- `app/api/routes/damages.py` - Rutas con consultas SQL directas
- `app/migrate.py` - Script de migración simple

### Instalación y configuración:

1. **Instalar dependencias:**
```bash
cd backend
pip install -e .
```

2. **Configurar base de datos:**
Crear archivo `.env` con:
```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=claims_db
POSTGRES_PORT=5432
```

3. **Crear tablas:**
```bash
python -m app.migrate
```

4. **Ejecutar aplicación:**
```bash
uvicorn app.main:app --reload
```

### Ventajas de esta implementación:

- **Simplicidad**: Menos dependencias y código más directo
- **Control**: Consultas SQL explícitas y optimizadas
- **Rendimiento**: Sin overhead del ORM
- **Mantenimiento**: Código más fácil de entender y debuggear

### API Endpoints:

- `GET /api/v1/claims/` - Listar reclamaciones
- `GET /api/v1/claims/{id}` - Obtener reclamación específica
- `POST /api/v1/claims/` - Crear reclamación
- `GET /api/v1/damages/` - Listar daños
- `POST /api/v1/damages/?claim_id={id}` - Crear daño