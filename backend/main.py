from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.core.database import engine, Base
from backend.core.database import SessionLocal, get_db
from backend.core.security import get_password_hash
import backend.models  # noqa: F401
from backend.models.user import User
from backend.routes import auth, clearance, department, certificate
from backend.services.certificate_service import CertificateService

# Create DB tables
Base.metadata.create_all(bind=engine)

def create_default_admin():
    if not settings.DEFAULT_ADMIN_EMAIL or not settings.DEFAULT_ADMIN_PASSWORD:
        return

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.DEFAULT_ADMIN_EMAIL).first()
        if existing:
            return
        db.add(User(
            name=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            role="ADMIN",
        ))
        db.commit()
    finally:
        db.close()

create_default_admin()

app = FastAPI(title="Digital No-Dues Clearance System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(department.router, prefix="/department", tags=["Department"])
app.include_router(clearance.router, prefix="/clearance", tags=["Clearance"])
app.include_router(certificate.router, prefix="/certificate", tags=["Certificate"])

@app.get("/verify/{certificate_id}")
def verify_certificate(certificate_id: str, db: Session = Depends(get_db)):
    return CertificateService.verify_certificate(db, certificate_id)

# Serve static files from frontend/dist
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        # Prevent catching API routes
        api_prefixes = ["auth/", "department/", "clearance/", "certificate/", "verify/", "docs", "openapi.json"]
        if any(full_path.startswith(prefix) for prefix in api_prefixes):
            return {"detail": "Not Found"}

        # Serve specific file if it exists (e.g. favicon.ico, manifest.json)
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Fallback to SPA index.html
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)

        return HTMLResponse(status_code=404, content="Frontend not built")
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Digital No-Dues Clearance System (Frontend not built)"}
