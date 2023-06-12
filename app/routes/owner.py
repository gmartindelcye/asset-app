from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.models.owner import Owner
from app.security.auth import get_session

router = APIRouter()


@router.get("/owners", response_model=List[Owner])
def get_owners(session: Session = Depends(get_session)):
    owners = session.exec(select(Owner)).all()
    return owners
