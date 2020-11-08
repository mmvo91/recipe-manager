from typing import Optional

from api.utils.schema import JSONModel


class Token(JSONModel):
    access_token: str
    token_type: str


class TokenData(JSONModel):
    username: Optional[str] = None
