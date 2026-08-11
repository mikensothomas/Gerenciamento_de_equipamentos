from pydantic import BaseModel, Field, EmailStr

class Agendar(BaseModel):
    id: int = Field(default=None, gt=10, description="Id do contato")
    email: EmailStr