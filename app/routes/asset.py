from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.models.asset import Asset
from app.security.auth import get_current_user
from app.services.auth import check_user_is_owner_or_admin, get_session

router = APIRouter()


@router.get("/assets", response_model=List[Asset])
def get_assets(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    assets = session.exec(select(Asset).where(check_user_is_owner_or_admin(current_user))).all()
    return assets