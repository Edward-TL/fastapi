from pydantic import BaseModel

class JWTUser(BaseModel):
    username: str
    password: str
    diasbled: bool = False
    role: str = None