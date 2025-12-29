from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    username = data.get("username")
    password = data.get("password")

    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}