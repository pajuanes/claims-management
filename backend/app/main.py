from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import claims, damages
from app.core.config import settings
from app.core.db import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Claims Manager API",
    description="Sistema de Gestión de Reclamaciones",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(claims.router, prefix=f"{settings.API_V1_STR}/claims", tags=["claims"])
app.include_router(damages.router, prefix=f"{settings.API_V1_STR}/damages", tags=["damages"])


@app.get("/")
async def root():
    return {"message": "Claims Manager API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}