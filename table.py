from pydantic import BaseModel

class Secret_creation(BaseModel):
    secret: str
    pass_phrase: str


class Secret_reveal(BaseModel):
    pass_phrase: str
    