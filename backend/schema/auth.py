from pydantic import BaseModel



class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class AuthRequest(BaseModel):
    email:str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str


class LogOutResposne(BaseModel):
    message: str
