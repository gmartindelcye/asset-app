# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserCreate
from app.security.auth import get_current_user, check_user_is_admin, get_password_hash
from db import a_session


router = APIRouter()


@router.post("/users")
def create_user(user: UserCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(a_session)):
    if not check_user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admin users can create new users")

    user.password = get_password_hash(user.password)
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
