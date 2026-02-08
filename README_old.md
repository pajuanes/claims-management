# Claims Manager — Sistema de Gestión de Reclamaciones — Caso Técnico Full Stack

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
- [API Endpoints](#api-endpoints)
- [Documentación Adicional](#documentación-adicional)

---

## Resumen

Este proyecto implementa un sistema de gestión de reclamaciones donde:

- Una **Reclamación** contiene información general (título, descripción, estado) y un **importe total calculado**.
- Una **Reclamación** tiene **Daños asociados**, cada uno con pieza, gravedad, imagen, precio y puntuación.
- En el detalle de una reclamación se muestra una **tabla de daños** y el **importe total se actualiza automáticamente** al crear/editar/eliminar daños.

---

## Requisitos funcionales

### Entidades

**Reclamación (Principal)**
- `title` (Título)
- `description` (Descripción)
- `status`: `PENDING` (Pendiente), `IN_REVIEW` (En Revisión), `FINALIZED` (Finalizado), `CANCELED` (Cancelado)
- `totalAmount` (Importe Total) **calculado**: suma de precios de daños

**Daño (Asociada)**
- `piece` (Pieza)
- `severity`: `LOW` (baja), `MEDIUM` (media), `HIGH` (alta)
- `imageUrl` (URL de la imagen)
- `price` (Precio numérico)
- `score` (Puntuación 1 a 10)

### Vistas Frontales
- Lista de Reclamaciones
- Detalle de la Reclamación
  - tabla de daños
  - total calculado
  - opción de añadir daños desde esta vista

---

## Reglas de negocio

1. **Validación de Daño (crear/editar)**  
   Todos los campos son obligatorios: `piece`, `severity`, `imageUrl`, `price`, `score`.

2. **Reactividad del total en detalle**  
   El **importe total** se actualiza automáticamente al:
   - añadir daño
   - eliminar daño
   - modificar el precio de un daño

3. **Restricciones de estado**
   - Los daños solo se pueden gestionar si la reclamación está en `PENDING`.
   - Una reclamación con al menos un daño `HIGH` requiere `description.length > 100` para pasar a `FINALIZED`.
   - El estado `CANCELED` solo es válido desde `PENDING`.

---

## Arquitectura y stack

### Backend
- **Python 3.11+**
- **FastAPI** (OpenAPI automático)
- **MongoDB** (base de datos)
- **psycopg** (driver)
- **pytest + httpx** (tests)
- **flake8** (calidad de código liviana)

### Frontend
- **Angular** (Reactive Forms + Router + HttpClient)
- Enfoque por **features** (Claims / Claim Detail / Damage form)

---

## 1. Visión general

Claims Manager permite a los gestores:

- Crear y gestionar **reclamaciones**
- Asociar múltiples **daños** a cada reclamación
- Visualizar en tiempo real el **importe total**
- Aplicar reglas de negocio según gravedad y estado

El sistema está construido con:
- Backend en **FastAPI + MongoDB**
- Frontend en **Angular**
- Enfoque **SDD (Specification-Driven Development)**
- Patrones de diseño modernos y arquitectura escalable
- Interfaces reactivas centradas en IA

---

## 2. Estructura del repositorio

claims-manager/
│
├── README.md
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── pyproject.toml
│   ├── .flake8
│   │
│   ├── app/
│   │   ├── main.py                # Entry point FastAPI
│   │   │
│   │   ├── core/                  # Infraestructura
│   │   │   ├── config.py           # Variables de entorno
│   │   │   └── db.py               # Conexión MongoDB
│   │   │
│   │   ├── domain/                # Modelo de dominio
│   │   │   └── models.py           # Claim, Damage, enums
│   │   │
│   │   ├── schemas/               # DTOs y validación
│   │   │   ├── claim.py
│   │   │   └── damage.py
│   │   │
│   │   ├── services/              # Reglas de negocio
│   │   │   └── claim_service.py
│   │   │
│   │   └── api/
│   │       ├── deps.py             # Inyección de dependencias
│   │       └── routes/
│   │           ├── claims.py
│   │           └── damages.py
│   │
│   └── tests/
│       └── test_health.py
│
└── frontend/
    ├── angular.json
    ├── package.json
    ├── tsconfig.app.json
    ├── tsconfig.json
    └── src/
        ├── app/
        │   ├── core/
        │   │   ├── models/
        │   │   └── services/
        │   │
        │   ├── features/
        │   │   └── claims/
        │   │       └── components/
        │   │           ├── claims-list/
        │   │           ├── claim-detail/
        │   │           ├── claim-form/
        │   │           └── damage-form/
        │   │
        │   ├── app.component.ts
        │   ├── app.config.ts
        │   └── app.routes.ts
        │
        ├── environments/
        │   └── environment/
        │
        ├── index.html
        ├── main.ts
        └── styles.css
---

## 3. Guía de usuario

### Lista de Reclamaciones
- Muestra todas las reclamaciones con:
  - Título
  - Estado
  - Importe total
- Desde aquí se puede navegar al detalle de una reclamación.

### Detalle de una Reclamación
Incluye:
- Información general (título, descripción, estado)
- Tabla de daños asociados
- Importe total calculado

### Gestión de daños
- Solo disponible si la reclamación está en estado **PENDING**
- Permite:
  - Añadir daño
  - Eliminar daño
- El total se actualiza automáticamente

### Cambio de estado
- Cancelar solo desde `PENDING`
- Para finalizar (`FINALIZED`) cuando hay daños `HIGH`, la descripción debe tener más de 100 caracteres

---

## 4. Guía de desarrollo

### Requisitos
- Docker + Docker Compose
- Python 3.11+
- Node.js 18+
- npm

---

## 4.1 Base de datos (MongoDB)

Levantar MongoDB con Docker:

```bash
docker compose up -d
```

---

## 4.2 Tests

### Tests Unitarios

Los tests unitarios no requieren que el servidor esté corriendo. Utilizan `AsyncClient` de `httpx` para simular las peticiones HTTP.

**Ejecutar tests unitarios:**

```bash
cd backend
pytest tests/test_unit.py -v
```

**Salida esperada:**
```
============================= test session starts =============================
platform win32 -- Python 3.10.8, pytest-9.0.2, pluggy-1.6.0
collected 2 items

tests/test_unit.py::test_health_check PASSED                             [ 50%]
tests/test_unit.py::test_root PASSED                                     [100%]

============================== 2 passed in 0.50s ==============================
```

**Tests incluidos:**
- `test_health_check`: Verifica endpoint `/health`
- `test_root`: Verifica endpoint `/` (root)

---

### Tests de Integración

Los tests de integración requieren que el servidor FastAPI esté corriendo. Realizan peticiones HTTP reales al servidor.

**Paso 1: Levantar el servidor FastAPI**

En una terminal:

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Paso 2: Ejecutar tests de integración**

En otra terminal:

```bash
cd backend
pytest tests/test_integration.py -v
```

**Configuración de URL:**

Por defecto, los tests usan `http://localhost:8000`. Para cambiar la URL:

```bash
API_BASE_URL=http://localhost:8000 pytest tests/test_integration.py -v
```

**Salida esperada:**
```
============================= test session starts =============================
platform win32 -- Python 3.10.8, pytest-9.0.2, pluggy-1.6.0
collected 2 items

tests/test_integration.py::test_health_check_integration PASSED          [ 50%]
tests/test_integration.py::test_root_integration PASSED                  [100%]

============================== 2 passed in 0.25s ==============================
```

---

### Ejecutar todos los tests

```bash
cd backend
pytest tests/ -v
```

### Tests con cobertura

```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

Esto genera un reporte HTML en `htmlcov/index.html` con la cobertura de código.

**Objetivo de cobertura:** 95%+

---