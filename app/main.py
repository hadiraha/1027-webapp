from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database import Base, engine, SessionLocal
from app.models import User
from app.auth import hash_password

Base.metadata.create_all(bind=engine)

def create_first_admin():
    db = SessionLocal()
    existing = db.query(User).filter(User.username == "admin").first()
    if existing is None:
        admin = User(
            username="admin",
            hashed_password=hash_password("123456"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("✔ First admin created → username: admin , password: 123456")
    else:
        print("✔ Admin already exists")
    db.close()

create_first_admin()

# ---------------------------
# FastAPI Init
# ---------------------------
app = FastAPI(title="Project System API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Routers Import
# ---------------------------
from app.routes_users import router as users_router
from app.routes_companies import router as companies_router

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(companies_router, prefix="/companies", tags=["companies"])


# Home redirect to login
@app.get("/")
def home():
    return {"status": "OK", "message": "Backend Running!"}


# ---------------------------
# Allow run via "python main.py"
# ---------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)