# Claims Manager - Full Stack SCRUM Plan

## Project Overview

**Project**: Claims Manager - Full Stack Application
**Stack**: 
- **Backend**: Node.js + Express + MongoDB + FastAPI (Python services)
- **Frontend**: Angular 19 + Standalone Components
**Duration**: Sprint 1 Completed
**Team Roles**: Full Stack Developer

---

## Sprint 1 Goals

### Backend
1. ✅ Implement REST API for Claims and Damages management
2. ✅ Configure MongoDB database with Mongoose schemas
3. ✅ Implement business rules validation
4. ✅ Create unit and integration tests
5. ✅ Setup code quality tools (flake8, pytest)
6. ✅ Configure CORS for Angular frontend integration

### Frontend
1. ✅ Setup Angular 19 with standalone components
2. ✅ Implement Claims list and detail views
3. ✅ Create reactive forms for Claims and Damages
4. ✅ Integrate with backend API
5. ✅ Implement EUR currency formatting
6. ✅ Add edit and delete functionality

---

## Product Backlog

### Epic 1: Database Setup (Backend)
- ✅ Configure MongoDB connection
- ✅ Create Claim schema with embedded Damages
- ✅ Setup environment variables (.env)
- ✅ Configure Docker Compose for MongoDB

### Epic 2: API Development (Backend)
- ✅ Implement Claims CRUD endpoints
- ✅ Implement Damages CRUD endpoints (nested routes)
- ✅ Add validation middleware
- ✅ Implement business rules service

### Epic 3: Business Rules (Backend)
- ✅ Validate damage fields (all required)
- ✅ Restrict damage management to PENDING status
- ✅ Validate status transitions
- ✅ Calculate total amount automatically

### Epic 4: Testing (Backend)
- ✅ Create unit tests (test_unit.py)
- ✅ Create integration tests (test_integration.py)
- ✅ Configure pytest with asyncio support
- ✅ Setup test environment

### Epic 5: Code Quality (Backend)
- ✅ Configure flake8 linting
- ✅ Setup pytest configuration
- ✅ Document API endpoints
- ✅ Add CORS middleware

### Epic 6: Frontend Setup
- ✅ Create Angular 19 project with standalone components
- ✅ Configure routing
- ✅ Setup HttpClient with interceptors
- ✅ Configure Spanish locale for EUR formatting
- ✅ Create core models and services

### Epic 7: Claims Management (Frontend)
- ✅ Implement claims-list component
- ✅ Implement claim-detail component
- ✅ Implement claim-form component
- ✅ Add delete claim functionality
- ✅ Display total amount in EUR

### Epic 8: Damages Management (Frontend)
- ✅ Implement damage-form component (create/edit)
- ✅ Add damage to claim
- ✅ Edit existing damage
- ✅ Delete damage
- ✅ Real-time total amount calculation
- ✅ Handle MongoDB $numberDecimal format

---

## Sprint Backlog

### User Stories Completed

#### US-001: As a developer, I need MongoDB connection
**Tasks**:
- ✅ Install motor (async MongoDB driver)
- ✅ Create db.py with connection functions
- ✅ Add MONGO_URI to environment variables
- ✅ Implement lifespan events in FastAPI

**Acceptance Criteria**:
- ✅ Connection established on startup
- ✅ Connection closed on shutdown
- ✅ Error handling implemented

---

#### US-002: As a user, I can create claims
**Tasks**:
- ✅ Create Claim model with Mongoose
- ✅ Implement POST /claims endpoint
- ✅ Add validation for required fields
- ✅ Return created claim with ID

**Acceptance Criteria**:
- ✅ Title is required
- ✅ Status defaults to PENDING
- ✅ Empty damages array initialized
- ✅ Returns 201 status code

---

#### US-003: As a user, I can view all claims
**Tasks**:
- ✅ Implement GET /claims endpoint
- ✅ Sort by creation date (newest first)
- ✅ Include damages count
- ✅ Calculate total amount

**Acceptance Criteria**:
- ✅ Returns array of claims
- ✅ Each claim includes damages
- ✅ Returns 200 status code

---

#### US-004: As a user, I can view claim details
**Tasks**:
- ✅ Implement GET /claims/:id endpoint
- ✅ Return 404 if not found
- ✅ Include all damages
- ✅ Calculate total amount

**Acceptance Criteria**:
- ✅ Returns complete claim object
- ✅ Includes embedded damages
- ✅ Returns 404 for invalid ID

---

#### US-005: As a user, I can delete claims
**Tasks**:
- ✅ Implement DELETE /claims/:id endpoint
- ✅ Cascade delete damages (automatic with MongoDB)
- ✅ Return 404 if not found
- ✅ Return 204 on success

**Acceptance Criteria**:
- ✅ Claim and damages deleted
- ✅ Returns 204 status code
- ✅ Returns 404 for invalid ID

---

#### US-006: As a user, I can add damages to claims
**Tasks**:
- ✅ Implement POST /claims/:id/damages endpoint
- ✅ Validate all required fields
- ✅ Check claim status is PENDING
- ✅ Return updated claim

**Acceptance Criteria**:
- ✅ All fields validated (part, severity, image_url, price, score)
- ✅ Only works for PENDING claims
- ✅ Returns complete updated claim
- ✅ Returns 409 if status not PENDING

---

#### US-007: As a user, I can edit damages
**Tasks**:
- ✅ Implement PUT /claims/:claimId/damages/:damageId endpoint
- ✅ Validate all required fields
- ✅ Check claim status is PENDING
- ✅ Return updated claim

**Acceptance Criteria**:
- ✅ Damage updated successfully
- ✅ Only works for PENDING claims
- ✅ Returns 404 if damage not found
- ✅ Returns complete updated claim

---

#### US-008: As a user, I can delete damages
**Tasks**:
- ✅ Implement DELETE /claims/:claimId/damages/:damageId endpoint
- ✅ Check claim status is PENDING
- ✅ Use deleteOne() instead of deprecated remove()
- ✅ Return 204 on success

**Acceptance Criteria**:
- ✅ Damage deleted successfully
- ✅ Only works for PENDING claims
- ✅ Returns 404 if damage not found
- ✅ Returns 204 status code

---

#### US-009: As a user, I can update claim status
**Tasks**:
- ✅ Implement PATCH /claims/:id/status endpoint
- ✅ Validate status transitions
- ✅ Check business rules (HIGH damage + description length)
- ✅ Call Python service for validation

**Acceptance Criteria**:
- ✅ Status updated successfully
- ✅ Business rules enforced
- ✅ Returns 409 for invalid transitions
- ✅ Returns updated claim

---

#### US-010: As a developer, I need unit tests
**Tasks**:
- ✅ Create test_unit.py
- ✅ Test /health endpoint
- ✅ Test / root endpoint
- ✅ Configure pytest.ini

**Acceptance Criteria**:
- ✅ Tests use AsyncClient
- ✅ Tests don't require running server
- ✅ All tests pass
- ✅ Coverage for health endpoints

---

#### US-011: As a developer, I need integration tests
**Tasks**:
- ✅ Create test_integration.py
- ✅ Use real server URL from environment
- ✅ Test against running server
- ✅ Add API_BASE_URL environment variable

**Acceptance Criteria**:
- ✅ Tests use httpx.AsyncClient
- ✅ Tests require running server
- ✅ URL configurable via environment
- ✅ Defaults to http://localhost:8000

---

#### US-012: As a user, I can view claims list (Frontend)
**Tasks**:
- ✅ Create claims-list component
- ✅ Fetch claims from API
- ✅ Display in grid layout
- ✅ Add delete button
- ✅ Format currency in EUR

**Acceptance Criteria**:
- ✅ Shows all claims
- ✅ Displays title, status, total, damages count
- ✅ Delete button works
- ✅ Currency formatted as EUR

---

#### US-013: As a user, I can view claim details (Frontend)
**Tasks**:
- ✅ Create claim-detail component
- ✅ Fetch claim by ID
- ✅ Display damages table
- ✅ Calculate total amount reactively
- ✅ Add/Edit/Delete damage buttons

**Acceptance Criteria**:
- ✅ Shows complete claim info
- ✅ Damages table with all fields
- ✅ Total updates automatically
- ✅ Edit/Delete only for PENDING status

---

#### US-014: As a user, I can create/edit damages (Frontend)
**Tasks**:
- ✅ Create damage-form component
- ✅ Implement reactive form validation
- ✅ Support create and edit modes
- ✅ Handle MongoDB price format
- ✅ Dynamic form title and button text

**Acceptance Criteria**:
- ✅ All fields validated
- ✅ Form resets after submit
- ✅ Shows "Add" or "Edit" based on mode
- ✅ Normalizes MongoDB $numberDecimal

---

#### US-015: As a user, I can delete damages (Frontend)
**Tasks**:
- ✅ Add delete button in damages table
- ✅ Confirm before delete
- ✅ Reload claim after delete
- ✅ Handle MongoDB _id field

**Acceptance Criteria**:
- ✅ Delete button visible for PENDING claims
- ✅ Confirmation dialog shown
- ✅ Table updates after delete
- ✅ Works with _id or id field

---

## Technical Decisions

### Backend Architecture
- **Node.js Backend**: Chosen over FastAPI for production (port 3000)
- **FastAPI**: Kept for Python services and validation logic
- **MongoDB**: Document database with embedded damages (no joins needed)
- **Mongoose**: ODM for schema validation and middleware

### Frontend Architecture
- **Angular 19**: Latest version with standalone components
- **Signals**: Reactive state management
- **Computed**: Automatic total amount calculation
- **Dynamic Imports**: Lazy loading for damage-form component
- **Spanish Locale**: EUR currency formatting

### Database Design
- **Embedded Documents**: Damages stored inside Claims (1-to-many relationship)
- **Automatic IDs**: MongoDB ObjectId for _id field
- **Decimal128**: Used for price precision
- **Timestamps**: Automatic createdAt and updatedAt

### API Design
- **RESTful**: Standard HTTP methods and status codes
- **Nested Routes**: /claims/:id/damages for damage operations
- **Validation**: express-validator middleware
- **Error Handling**: Consistent error responses with error field

### Testing Strategy
- **Unit Tests**: Mock-free tests using FastAPI TestClient
- **Integration Tests**: Real HTTP requests to running server
- **Async Tests**: pytest-asyncio for async/await support
- **Separation**: test_unit.py vs test_integration.py

---

## Definition of Done

- ✅ Code written and committed
- ✅ Unit tests written and passing
- ✅ Integration tests written
- ✅ Code passes flake8 linting
- ✅ API documented in README
- ✅ Environment variables documented
- ✅ CORS configured for frontend
- ✅ Error handling implemented
- ✅ Business rules validated

---

## Retrospective

### What Went Well
- MongoDB embedded documents simplified data model
- Mongoose validation reduced boilerplate code
- Async/await pattern consistent throughout
- Test separation (unit vs integration) clear
- CORS configuration straightforward

### What Could Be Improved
- Add more comprehensive test coverage
- Implement request/response logging
- Add API rate limiting
- Implement authentication/authorization
- Add database migrations strategy

### Action Items
- [ ] Increase test coverage to 95%+
- [ ] Add logging middleware
- [ ] Document all API endpoints with OpenAPI
- [ ] Add health check for MongoDB connection
- [ ] Implement CI/CD pipeline

---

## API Endpoints Summary

### Claims
- `GET /api/v1/claims` - List all claims
- `GET /api/v1/claims/:id` - Get claim by ID
- `POST /api/v1/claims` - Create new claim
- `PATCH /api/v1/claims/:id/status` - Update claim status
- `DELETE /api/v1/claims/:id` - Delete claim

### Damages
- `POST /api/v1/claims/:id/damages` - Add damage to claim
- `PUT /api/v1/claims/:claimId/damages/:damageId` - Update damage
- `DELETE /api/v1/claims/:claimId/damages/:damageId` - Delete damage

### Health
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with version info

---

## Environment Variables

```env
MONGO_URI=mongodb://localhost:27017/claims_db
PORT=3000
NODE_ENV=development
API_BASE_URL=http://localhost:3000
```

---

## Running Tests

### Unit Tests (No server required)
```bash
cd backend
pytest tests/test_unit.py -v
```

### Integration Tests (Server must be running)
```bash
# Terminal 1: Start server
cd backend/node-backend
npm start

# Terminal 2: Run tests
cd backend
API_BASE_URL=http://localhost:3000 pytest tests/test_integration.py -v
```

### All Tests
```bash
cd backend
pytest tests/ -v
```

### With Coverage
```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

---

## Code Quality

### Linting
```bash
cd backend
flake8 app/ --max-line-length=120
```

### Type Checking (if using mypy)
```bash
cd backend
mypy app/
```

---

## Next Sprint Planning

### Proposed Features
1. Authentication & Authorization (JWT)
2. File upload for damage images
3. Pagination for claims list
4. Search and filter capabilities
5. Audit log for changes
6. Email notifications
7. Export claims to PDF
8. Dashboard with statistics

### Technical Debt
1. Add comprehensive logging
2. Implement rate limiting
3. Add request validation schemas
4. Improve error messages
5. Add API documentation (Swagger/OpenAPI)
6. Setup CI/CD pipeline
7. Add database indexes for performance
8. Implement caching strategy
