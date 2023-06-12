from typing import Optional
from sqlmodel import Field, SQLModel


class AssetType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    template_info: Optional[str]