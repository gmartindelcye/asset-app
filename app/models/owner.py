from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from asset import Asset


class Owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    assets: List["Asset"] = Relationship(back_populates="asset")


