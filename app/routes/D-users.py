from fastapi import APIRouter, Depends
from app import crud, schemas, auth
from sqlalchemy.orm import Session
from app.database import get_db
from jose import jwt
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, data)

@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(auth.User).filter(auth.User.username == data.username).first()
    if not user or not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid login")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}