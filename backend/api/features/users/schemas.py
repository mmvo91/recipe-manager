from api.utils.schema import JSONModel


class UserBase(JSONModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    active: bool

    class Config:
        orm_mode = True
