from sqlalchemy.orm import Session

from apps.models import UserDB
from apps.schemas import UserCreate, UserResponse, UserLogin
from apps.security import create_access_token, hash_password, verify_password


def create_user(db: Session, user: UserCreate) -> UserResponse:

    existing_user = (
        db.query(UserDB).filter(UserDB.email == user.email).first()
    )

    if existing_user:
        raise ValueError("Email already registered")
    
    existing_username = (
    db.query(UserDB)
      .filter(UserDB.username == user.username)
      .first()
      )

    if existing_username:

        raise ValueError("Username already taken")
    
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email
    )
def login_user(db: Session, user: UserLogin):
    print("=" * 50)
    print("Input Email:", repr(user.email))
    print("Input Password:", repr(user.password))

    db_user = db.query(UserDB).filter(
        UserDB.email == user.email
    ).first()

    print("DB User:", db_user)

    if db_user:
        print("DB Email:", db_user.email)
        print("DB Hash:", db_user.hashed_password)

        result = verify_password(
            user.password,
            db_user.hashed_password
        )

        print("Verify Result:", result)

    print("=" * 50)

    if not db_user:
        raise ValueError("Invalid email or password")

    if not verify_password(user.password, db_user.hashed_password):
        raise ValueError("Invalid email or password")

    access_token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }