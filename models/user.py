from pydantic import BaseModel
import enum
from fastapi import Query

class Role(str, enum.Enum):
    admin = "admin"
    personel = "personel" 

class User(BaseModel):
    name: str
    password: str
    mail: str = Query(..., regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    role: Role
