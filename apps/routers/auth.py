from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.schemas import UserLogin
from apps.services.user_service import login_user
from apps.database import get_db
from apps.schemas import UserCreate
from apps.services.user_service import create_user

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(    user: UserCreate,    db: Session = Depends(get_db)):
    try:
        return create_user(db, user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.post("/login")
def login(user: UserLogin,
          db: Session = Depends(get_db)):
    return login_user(db, user)