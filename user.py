from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str
    lastname: str
    identity_number: str
    phone: str
    email: str
