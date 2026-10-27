from sqlmodel import SQLModel, Field
from datetime import datetime

class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_token"
    id: int | None = Field(default=None, primary_key=True)
    jti: str = Field(max_length=36, unique=True, index=True, nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked_at: datetime = Field(nullable=False)