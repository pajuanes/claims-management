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
│   │   ├── core/               # Config & DB
│   │   ├── domain/             # Models
│   │   └── api/routes/         # Endpoints
│   │
│   ├── node-backend/           # Node.js API (production)
│   │   └── src/
│   │       ├── models/         # Mongoose schemas
│   │       ├── controllers/    # Business logic
│   │       ├── routes/         # API routes
│   │       └── services/       # External services
│   │
│   └── tests/
│       ├── test_unit.py        # Unit tests
│       └── test_integration.py # Integration tests
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
