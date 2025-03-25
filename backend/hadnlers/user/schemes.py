from pydantic import BaseModel, PositiveInt


class UserScheme(BaseModel):
    chat_id: str


class ReturnUser(UserScheme):
    id: PositiveInt
