from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool

class UpdateMeIn(BaseModel):
    email: EmailStr | None = None

class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)

class AdminSetRoleIn(BaseModel):
    role: str = Field(pattern="^(user|admin)$")

class AdminDisableIn(BaseModel):
    is_active: bool
