from typing import Optional
from pydantic import BaseModel

class Pokemon(BaseModel):
    id: Optional[int] = None
    nome: str 
    elemento: str 
    altura: int