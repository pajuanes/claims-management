# Claims Manager — Sistema de Gestión de Reclamaciones

Herramienta **Full Stack** para gestores de reclamaciones que permite crear y gestionar **reclamaciones** con **múltiples daños asociados**, diseñada con **arquitectura escalable**, aplicando **reglas de negocio**, **reactividad en UI** y un enfoque **SDD (Specification-Driven Development)**.

---

## Índice

- [Resumen](#resumen)
- [Requisitos Funcionales](#requisitos-funcionales)
- [Reglas de Negocio](#reglas-de-negocio)
- [Arquitectura y Stack](#arquitectura-y-stack)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Guía de Desarrollo](#guía-de-desarrollo)
  - [Prerequisitos](#prerequisitos)
  - [Base de Datos](#base-de-datos)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Tests](#tests)
    - [Tests Unitarios](#tests-unitarios)
    - [Tests de Integración](#tests-de-integración)
    - [Todos los Tests](#todos-los-tests)
    - [Tests con Cobertura](#tests-con-cobertura)
- [API Endpoints](#api-endpoints)
- [CI/CD Pipeline](#cicd-pipeline)
- [Documentación Adicional](#documentación-adicional)

---

## Resumen

Sistema de gestión de reclamaciones con:

- **Reclamaciones**: título, descripción, estado e importe total calculado automáticamente
- **Daños asociados**: pieza, gravedad, imagen, precio y puntuación
- **Reactividad**: el importe total se actualiza automáticamente al crear/editar/eliminar daños
- **Reglas de negocio**: validaciones según estado y gravedad

---

## Requisitos Funcionales

### Entidades

**Reclamación**
- `title` (Título)
- `description` (Descripción)
- `status`: `PENDING`, `IN_REVIEW`, `FINALIZED`, `CANCELED`
- `totalAmount` (calculado): suma de precios de daños

**Daño**
- `part` (Pieza)
- `severity`: `LOW`, `MEDIUM`, `HIGH`
- `image_url` (URL de la imagen)
- `price` (Precio numérico)
- `score` (Puntuación 1-10)

### Funcionalidades

- Listar reclamaciones con total y estado
- Ver detalle de reclamación con tabla de daños
- Crear/editar/eliminar reclamaciones
- Añadir/editar/eliminar daños (solo en estado PENDING)
- Cambiar estado de reclamación

---

## Reglas de Negocio

1. **Validación de Daño**: Todos los campos obligatorios (`part`, `severity`, `image_url`, `price`, `score`)

2. **Reactividad del Total**: Se actualiza automáticamente al añadir/eliminar/modificar daños

3. **Restricciones de Estado**:
   - Daños solo gestionables en estado `PENDING`
   - Reclamación con daño `HIGH` requiere `description.length > 100` para `FINALIZED`
   - Estado `CANCELED` solo válido desde `PENDING`

---

## Arquitectura y Stack

### Backend
- **Node.js + Express** (API REST - puerto 3000)
- **FastAPI + Python** (Servicios de validación - puerto 8000)
- **MongoDB** (base de datos con Mongoose)
- **pytest + httpx** (tests)

### Frontend
- **Angular 19** (Standalone Components)
- **Signals** (Reactive state management)
- **Reactive Forms** (Validación)
- **Spanish Locale** (EUR currency formatting)

---

## Estructura del Repositorio

```
claims-management/
├── README.md
├── SCRUM.md                    # Plan de trabajo
├── AI_LOG.md                   # Uso de IA en el proyecto
├── .gitignore                  # Archivos excluidos de Git
├── LICENSE                     # Licencia MIT
├── docker-compose.yml
│
├── backend/
│   ├── app/                    # FastAPI application
│   │   ├── main.py
│   │   ├── migrate.py          # Database migrations
│   │   ├── core/               # Config & DB
│   │   │   ├── config.py       # Settings & Vault integration
│   │   │   └── db.py           # MongoDB connection & queries
│   │   ├── schemas/            # Pydantic models
│   │   │   └── models.py       # Data validation models
│   │   └── api/routes/         # Endpoints
│   │       ├── claims.py       # Claims endpoints
│   │       └── damages.py      # Damages endpoints
│   │
│   ├── node-backend/           # Node.js API (production)
│   │   └── src/
│   │       ├── models/         # Mongoose schemas
│   │       ├── controllers/    # Business logic
│   │       ├── routes/         # API routes
│   │       └── services/       # External services
│   │
│   └── tests/                  # Test suite
│       ├── test_unit.py        # Basic unit tests
│       ├── test_integration.py # Integration tests (require server)
│       ├── test_claims_router.py    # Claims endpoints coverage
│       ├── test_damages_router.py   # Damages endpoints coverage
│       ├── test_config.py      # Config & Vault tests
│       ├── test_db.py          # Database functions tests
│       ├── test_main.py        # Lifespan & app tests
│       ├── test_migrate.py     # Migration tests
│       └── test_models.py      # Pydantic models tests
│
└── frontend/
    └── src/app/
        ├── core/
        │   ├── models/         # TypeScript interfaces
        │   └── services/       # HTTP services
        └── features/claims/
            └── components/     # Claims & Damages components
```

---

## Guía de Desarrollo

### Prerequisitos

- Docker + Docker Compose
- Python 3.10+
- Node.js 18+
- npm
- Git

### Clonar Repositorio

```bash
git clone <repository-url>
cd claims-management
```

**Nota**: El proyecto incluye `.gitignore` que excluye:
- Dependencias (`node_modules/`, `venv/`)
- Archivos de entorno (`.env`)
- Archivos generados (`dist/`, `__pycache__/`)
- Configuraciones de IDE (`.vscode/`, `.idea/`)

### Base de Datos

Levantar MongoDB con Docker:

```bash
docker compose up -d
```

### Backend

**Instalar dependencias Python:**

```bash
cd backend
pip install motor pydantic-settings fastapi uvicorn pytest httpx pytest-asyncio
```

**Levantar servidor Node.js (puerto 3000):**

```bash
cd backend/node-backend
npm install
npm start
```

**Levantar servidor FastAPI (puerto 8000):**

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

**Instalar dependencias:**

```bash
cd frontend
npm install
```

**Levantar servidor de desarrollo:**

```bash
npm start
```

Acceder a: `http://localhost:4200`

### Tests

#### Tests Unitarios

No requieren servidor corriendo. Usan `AsyncClient` para simular peticiones HTTP.

```bash
cd backend
pytest tests/test_unit.py -v
```

**Tests incluidos:**
- `test_health_check`: Verifica endpoint `/health`
- `test_root`: Verifica endpoint `/` (root)

#### Tests de Cobertura

Tests completos que cubren todos los módulos de la aplicación:

**Claims Router (`test_claims_router.py`):**
```bash
pytest tests/test_claims_router.py -v
```
- GET claims (vacío y con datos)
- POST crear claim
- PATCH actualizar estado
- Validaciones: claim not found, estado inválido, descripción corta con HIGH damage

**Damages Router (`test_damages_router.py`):**
```bash
pytest tests/test_damages_router.py -v
```
- GET damages (vacío y con datos)
- POST crear damage
- PUT actualizar damage
- DELETE eliminar damage
- Validaciones: claim not found, claim not PENDING, errores de base de datos

**Config (`test_config.py`):**
```bash
pytest tests/test_config.py -v
```
- get_secret_key desde settings
- get_secret_key desde Vault
- Fallback a variable de entorno
- Fallback a valor por defecto

**Database (`test_db.py`):**
```bash
pytest tests/test_db.py -v
```
- Conexión y desconexión MongoDB
- execute_query, execute_one
- insert_one, insert_many
- find_one, find_many (con/sin límite)
- update_one, update_many
- delete_one, delete_many

**Main (`test_main.py`):**
```bash
pytest tests/test_main.py -v
```
- Lifespan startup/shutdown

**Migrate (`test_migrate.py`):**
```bash
pytest tests/test_migrate.py -v
```
- Creación de tablas claims y damages

**Models (`test_models.py`):**
```bash
pytest tests/test_models.py -v
```
- Enums: ClaimStatus, DamageSeverity
- normalize_price (float, int, string, Decimal)
- Validaciones: score, price
- total_amount property

#### Tests de Integración

Requieren servidor FastAPI corriendo. Realizan peticiones HTTP reales.

**Terminal 1 - Levantar servidor:**

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Ejecutar tests:**

```bash
cd backend
pytest tests/test_integration.py -v
```

**Configurar URL personalizada:**

```bash
API_BASE_URL=http://localhost:8000 pytest tests/test_integration.py -v
```

**Nota:** Los tests de integración se saltan automáticamente si el servidor no está corriendo.

#### Todos los Tests

```bash
cd backend
pytest tests/ -v
```

#### Tests con Cobertura

```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

Genera reporte HTML en `htmlcov/index.html`

**Objetivo de cobertura:** 95%+

**Cobertura actual por módulo:**
- `app/api/routes/claims.py`: 96%+
- `app/api/routes/damages.py`: 100%
- `app/core/config.py`: 100%
- `app/core/db.py`: 100%
- `app/schemas/models.py`: 100%
- `app/main.py`: 100%
- `app/migrate.py`: 100%

---

## API Endpoints

### Claims

- `GET /api/v1/claims` - Listar reclamaciones
- `GET /api/v1/claims/:id` - Obtener reclamación por ID
- `POST /api/v1/claims` - Crear reclamación
- `PATCH /api/v1/claims/:id/status` - Actualizar estado
- `DELETE /api/v1/claims/:id` - Eliminar reclamación

### Damages

- `POST /api/v1/claims/:id/damages` - Añadir daño
- `PUT /api/v1/claims/:claimId/damages/:damageId` - Actualizar daño
- `DELETE /api/v1/claims/:claimId/damages/:damageId` - Eliminar daño

### Health

- `GET /health` - Health check
- `GET /` - Root endpoint con versión

---

## CI/CD Pipeline

### Workflows Automáticos

El proyecto incluye dos workflows de GitHub Actions:

1. **`.github/workflows/ci-cd.yml`**: Testing, building y release tags
2. **`.github/workflows/deploy-pages.yml`**: Despliegue a GitHub Pages

Ambos se ejecutan automáticamente en push a rama `main`.

### Proceso del Pipeline

#### 1. Job: Test

**Pasos ejecutados:**

1. **Setup**: Configura Python 3.10 y Node.js 18
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   npm run install:backend
   npm run install:frontend
   ```
3. **Ejecutar tests backend**:
   ```bash
   cd backend
   pytest tests/test_unit.py -v --cov=app --cov-report=term
   ```
   - Solo ejecuta tests unitarios (no requieren servidor)
   - Cobertura objetivo: 95%+
   - Si los tests fallan, el pipeline se detiene
4. **Build frontend**:
   ```bash
   npm run build:frontend
   ```
   - Si el build falla, el pipeline se detiene

#### 2. Job: Deploy (solo rama `main`)

**Requisitos:**
- Job `test` debe completarse exitosamente
- Solo se ejecuta en push a rama `main`

**Pasos ejecutados:**

1. **Deploy to production**: Placeholder para comandos de despliegue
2. **Create release tag**: Genera tag automático con formato `vYYYY.MM.DD-HHMMSS`

### Ejecución Manual del Workflow

Para simular el workflow localmente:

```bash
# 1. Instalar dependencias
pip install -r requirements.txt
npm run install:backend
npm run install:frontend

# 2. Levantar MongoDB
docker compose up -d

# 3. Ejecutar tests
cd backend
pytest tests/test_unit.py -v --cov=app --cov-report=term

# 4. Build frontend
cd ..
npm run build:frontend
```

### Manejo de Errores

El pipeline está configurado para **detenerse inmediatamente** si ocurre algún error:

- **Tests fallan**: El job `test` falla y no se ejecuta `deploy`
- **Build falla**: El job `test` falla y no se ejecuta `deploy`
- **Deploy falla**: Se notifica el error pero no afecta al tag

### Verificar Estado del Pipeline

1. Ir a la pestaña **Actions** en GitHub
2. Ver el estado de cada workflow:
   - ✅ Verde: Exitoso
   - ❌ Rojo: Fallido
   - 🟡 Amarillo: En progreso
3. Click en el workflow para ver logs detallados de cada paso

### GitHub Pages Deployment

El workflow `deploy-pages.yml` despliega automáticamente el frontend en GitHub Pages.

**Configuración requerida:**

1. Ve a `Settings` > `Pages`
2. En `Source`, selecciona `GitHub Actions`
3. Guarda los cambios

**Proceso automático:**

1. **Build job**: Instala dependencias y construye frontend con `--configuration=production --base-href=/claims-management/`
2. **Deploy job**: Despliega artifact a GitHub Pages

**Ejecución manual:**

Puedes ejecutar el workflow manualmente desde la pestaña `Actions` > `Deploy to GitHub Pages` > `Run workflow`

**Limitaciones:**

- GitHub Pages solo sirve archivos estáticos (HTML/CSS/JS)
- No puede ejecutar el backend Node.js ni conectarse a MongoDB
- Requiere backend desplegado en servicio externo (Railway, Render, AWS, etc.)
- Actualizar `frontend/src/environments/environment.prod.ts` con URL del backend en producción

### Configuración de Secretos

Para habilitar despliegue automático, configurar **Repository secrets** en GitHub:

1. Ir a `Settings` > `Secrets and variables` > `Actions` > `Repository secrets`
2. Click en `New repository secret`
3. Añadir los siguientes secretos (si son necesarios):

**Secretos recomendados:**

- `DOCKER_USERNAME`: Usuario de Docker Hub (para build de imágenes)
- `DOCKER_PASSWORD`: Token de acceso de Docker Hub
- `AWS_ACCESS_KEY_ID`: Credenciales AWS (si se despliega en AWS)
- `AWS_SECRET_ACCESS_KEY`: Secret key de AWS
- `MONGO_URI_PROD`: URI de MongoDB en producción

**Nota**: Los secretos de repositorio están disponibles para todas las ramas. Si necesitas secretos específicos por entorno (staging/production), usa **Environment secrets** en su lugar.

---

## Documentación Adicional

- **[SCRUM.md](./SCRUM.md)**: Plan de trabajo completo con sprints, user stories y retrospectiva
- **[AI_LOG.md](./AI_LOG.md)**: Documentación del uso de IA (Amazon Q Developer) en el proyecto
- **Backend Tests**: Documentación detallada de tests unitarios e integración en este README

---

## Tecnologías y Patrones

- **SDD (Specification-Driven Development)**: Contrato API definido antes del desarrollo
- **Embedded Documents**: Daños almacenados dentro de Claims (MongoDB)
- **Reactive State**: Signals y Computed properties (Angular 19)
- **Lazy Loading**: Dynamic imports para componentes
- **Validation**: express-validator (backend) + Reactive Forms (frontend)
- **Type Safety**: TypeScript strict mode + Pydantic models

---

## Autor

**Pablo García Juanes**  
Email: apps@pablogarciajuanes.com

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](./LICENSE) para más detalles.

**Nota**: Este proyecto fue desarrollado como caso técnico para un proceso de selección.
