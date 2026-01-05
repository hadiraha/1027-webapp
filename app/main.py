from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import RedirectResponse
from app.database import Base, engine, SessionLocal
from app.models import User
from app.auth import hash_password

Base.metadata.create_all(bind=engine)

def create_first_admin():
    db = SessionLocal()
    try:
        admin_exists = db.query(User).filter(User.username == "admin").first()
        if not admin_exists:
            admin = User(
                username="admin",
                hashed_password=hash_password("123456"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Default admin created (username: admin | password: 123456)")
        else:
            print("Admin already exists")
    except Exception as e:
        print("Failed to create admin:", e)
    finally:
        db.close()


create_first_admin()


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


from app.routes_users import router as users_router
from app.routes_companies import router as companies_router

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(companies_router, prefix="/companies", tags=["Companies"])
 

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/static/login.html")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)