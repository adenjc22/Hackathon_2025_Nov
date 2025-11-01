from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.uploads import router as uploads_router

app = FastAPI(
    title="Legacy Album API",
    version="0.1.0",
    description="Phase 1: FastAPI app structure with CORS and base routes."
)

# Allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Legacy Album API running"}

# Include sub-routers
app.include_router(health_router, prefix="/api/health", tags=["Health"])
app.include_router(uploads_router, prefix="/api/uploads", tags=["Uploads"])
