from typing import Optional
from sqlmodel import Field, SQLModel


class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int
    description: str
    price: float
    date_of_acquisition: str
    additional_info: Optional[str]


